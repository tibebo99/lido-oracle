from time import sleep
from typing import Optional, List

from prometheus_client import start_http_server
from web3 import Web3
from web3_multi_provider import MultiProvider

from src import variables
from src.contracts import contracts
from src.metrics.logging import logging
from src.metrics.healthcheck_server import start_pulse_server, pulse
from src.modules.ejection import Ejector
from src.modules.interface import OracleModule
from src.protocol_upgrade_checker import wait_for_withdrawals
from src.providers.beacon import BeaconChainClient
from src.providers.typings import Epoch
from src.variables import DAEMON, WEB3_PROVIDER_URIS, BEACON_NODE

logger = logging.getLogger(__name__)


class Oracle:
    _last_finalized_epoch: Epoch = 0

    def __init__(self, web3: Web3, beacon_chain_client: BeaconChainClient):
        self._w3 = web3
        self._beacon_chain_client = beacon_chain_client

        self.modules: List[OracleModule] = [
            # Accounting(self._w3, self._beacon_chain_client),
            Ejector(self._w3, self._beacon_chain_client),
        ]

        self.epochs_per_frame, self.slots_per_epoch, self.seconds_per_slot, self.genesis_time = contracts.oracle.functions.getBeaconSpec().call()

    def run_as_daemon(self):
        while True:
            pulse()
            logger.info({'msg': 'Run cycle.'})
            self.run_cycle()

    def run_cycle(self):
        epoch = self._fetch_next_finalized_epoch()
        logger.info({'msg': 'Get finalized epoch.', 'value': epoch})

        try:
            self.run_once(epoch)
        except KeyboardInterrupt as error:
            logger.error({'msg': 'Key interrupt.', 'error': error})
            raise KeyboardInterrupt from error
        except Exception as error:
            logger.error({'msg': 'Unexpected exception.', 'error': error})
            raise Exception from error

    def _fetch_next_finalized_epoch(self) -> Epoch:
        while True:
            current_finalized_epoch = Epoch(int(self._beacon_chain_client.get_head_finality_checkpoints()['finalized']['epoch']))

            if current_finalized_epoch > self._last_finalized_epoch:
                self._last_finalized_epoch = current_finalized_epoch

                return current_finalized_epoch
            else:
                sleep(self.slots_per_epoch * self.seconds_per_slot)

    def run_once(self, epoch: Optional[Epoch] = None):
        if epoch is None:
            epoch = self._beacon_chain_client.get_head_finality_checkpoints()['finalized']['epoch']

        slot = epoch * self.slots_per_epoch

        logger.info({'msg': 'Execute all modules.', 'epoch': epoch, 'slot': slot})

        block_hash = self._beacon_chain_client.get_block_details(
            slot,
            get_next_if_missed=True,
        )['message']['body']['eth1_data']['block_hash']
        logger.info({'msg': 'Fetch execution block hash.', 'value': block_hash})

        for module in self.modules:
            try:
                module.run_module(slot, block_hash)
            except Exception as error:
                logger.error({'msg': f'Module {module.__class__.__name__} failed.', 'error': str(error)})


if __name__ == '__main__':
    logger.info({'msg': 'Oracle startup.'})

    logger.info({'msg': f'Start healthcheck server for Docker container on port {variables.HEALTHCHECK_SERVER_PORT}'})
    start_pulse_server()

    logger.info({'msg': f'Start http server with prometheus metrics on port {variables.PROMETHEUS_PORT}'})
    start_http_server(variables.PROMETHEUS_PORT)

    logger.info({'msg': 'Initialize multi web3 provider.'})
    w3 = Web3(MultiProvider(WEB3_PROVIDER_URIS))

    logger.info({'msg': 'Check protocol version.'})
    wait_for_withdrawals(w3)

    logger.info({'msg': 'Initialize contracts.'})
    contracts.initialize(w3)

    logger.info({'msg': 'Initialize Consensus Layer client.'})
    beacon_client = BeaconChainClient(BEACON_NODE)

    logger.info({'msg': 'Initialize Oracle.'})
    oracle = Oracle(w3, beacon_client)

    if DAEMON:
        logger.info({'msg': 'Run Oracle as Daemon.'})
        oracle.run_as_daemon()
    else:
        logger.info({'msg': 'Run Oracle once.'})
        oracle.run_cycle()
