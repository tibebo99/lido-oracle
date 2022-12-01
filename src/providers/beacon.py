from typing import Optional, List
from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.metrics.logging import logging
from src.providers.typings import StateFinalityCheckpoints, Validator, SignedBeaconBlock

logger = logging.getLogger(__name__)


class BeaconChainClient:
    """
    API specifications can be found here
    https://ethereum.github.io/beacon-APIs/
    """
    REQUEST_TIMEOUT = 300

    api_beacon_head_finality_checkpoints = 'eth/v1/beacon/states/head/finality_checkpoints'
    api_get_validators = 'eth/v1/beacon/states/{}/validators'
    api_get_block_details = 'eth/v2/beacon/blocks/{}'

    def __init__(self, host: str):
        self.host = host

        retry_strategy = Retry(
            total=5,
            status_forcelist=[418, 429, 500, 502, 503, 504],
            backoff_factor=5,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, url: str, params: Optional[dict] = None) -> dict | list:
        response = self.session.get(
            urljoin(self.host, url),
            params=params,
            timeout=self.REQUEST_TIMEOUT,
        )

        try:
            data = response.json()['data']
        except KeyError as error:
            msg = f'Response [{response.status_code}] with text: {str(response.text)} was returned.'
            logger.error(msg)
            raise KeyError(msg) from error
        except BaseException as error:
            print(response.text)
            print(urljoin(self.host, url))
            raise error

        return data

    def get_head_finality_checkpoints(self) -> StateFinalityCheckpoints:
        """Spec: https://ethereum.github.io/beacon-APIs/#/Beacon/getStateFinalityCheckpoints"""
        return self._get(self.api_beacon_head_finality_checkpoints)

    def get_validators(self, slot: int, pub_keys: Optional[str] = None) -> List[Validator]:
        """Spec: https://ethereum.github.io/beacon-APIs/#/Beacon/getStateValidators"""
        return self._get(self.api_get_validators.format(slot), params={'id': pub_keys})

    def get_block_details(self, slot: int, get_next_if_missed: True) -> SignedBeaconBlock:
        """Spec: https://ethereum.github.io/beacon-APIs/#/Beacon/getBlockV2"""

        if get_next_if_missed:
            for i in range(32):
                try:
                    return self._get(self.api_get_block_details.format(slot + i))
                except KeyError:
                    logger.warning({'msg': 'Try to get next slot.', 'value': slot + i})

        else:
            return self._get(self.api_get_block_details.format(slot))

