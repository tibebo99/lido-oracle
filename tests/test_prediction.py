import pytest
from typings import BlockStamp, SlotNumber
from unittest.mock import MagicMock, ANY
from web3.types import Wei
from src.modules.accounting.prediction import Prediction


@pytest.fixture()
def tr_hashes():
    return ['7f8fcaef4faa91a78c14c3eac86542', '07839b77ec9b93c95747b8de05ba03', '9f8018bbabd97cd3f0d27007a8d11a',
            '3472fd40eb87b8dd1069da56daaa17', '7c3a071c009b8eb39d07fb27c51fa1', '2335edcb12bf3e7a530f81d1bb46d7',
            '6b02f3dcfc5ea65e7ade78c38d3a59', '2d558d71920bc6b8344acfcdd5b587', '2f7d722b4584d3a053258f5c985fd2',
            '749390e4da86fae90b2bea60af3459', '184d9f0810ea02e20eef711f39a6eb', '3f319d0cef2d4150ff3c63d87262a6',
            '4e23a53dc4e940317f3f54be2a5662']


@pytest.fixture()
def eth_distributed_logs(tr_hashes):
    return [
        {
            'transactionHash': tr_hashes[0],
            'args': {
                'reportTimestamp': 1675441364,
                'withdrawalsWithdrawn': Wei(500000000000000000),
                'executionLayerRewardsWithdrawn': Wei(500000000000000000),
            }
        },
        {
            'transactionHash': tr_hashes[1],
            'args': {
                'reportTimestamp': 1675441376,
                'withdrawalsWithdrawn': Wei(5000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(400000000000000000),
            }
        },
        {
            'transactionHash': tr_hashes[2],
            'args': {
                'reportTimestamp': 1675441388,
                'withdrawalsWithdrawn': Wei(7000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(700000000000000000),
            }
        },
        {
            'transactionHash': tr_hashes[3],
            'args': {
                'reportTimestamp': 1675441400,
                'withdrawalsWithdrawn': Wei(9000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(900000000000000000),
            }
        },
        {

            'transactionHash': tr_hashes[4],
            'args': {
                'reportTimestamp': 1675441424,
                'withdrawalsWithdrawn': Wei(1000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(100000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[5],
            'args': {
                'reportTimestamp': 1675441436,
                'withdrawalsWithdrawn': Wei(11000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(1100000000000000000),
            }
        },
        {
            'transactionHash': tr_hashes[6],
            'args': {
                'reportTimestamp': 1675441448,
                'withdrawalsWithdrawn': Wei(14000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(1400000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[7],
            'args': {
                'reportTimestamp': 1675441460,
                'withdrawalsWithdrawn': Wei(15000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(1500000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[8],
            'args': {
                'reportTimestamp': 1675441472,
                'withdrawalsWithdrawn': Wei(17000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(1700000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[9],
            'args': {
                'reportTimestamp': 1675441484,
                'withdrawalsWithdrawn': Wei(21000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(21000000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[10],
            'args': {
                'reportTimestamp': 1675441496,
                'withdrawalsWithdrawn': Wei(32000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(32000000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[11],
            'args': {
                'reportTimestamp': 1675441508,
                'withdrawalsWithdrawn': Wei(64000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(64000000000000000000),
            }
        }
        ,
        {
            'transactionHash': tr_hashes[12],
            'args': {
                'reportTimestamp': 1675441520,
                'withdrawalsWithdrawn': Wei(132000000000000000000),
                'executionLayerRewardsWithdrawn': Wei(132000000000000000000),
            }
        }
    ]


@pytest.fixture()
def token_rebased_logs(tr_hashes):
    return [
        {
            'transactionHash': tr_hashes[0],
            'args': {
                'reportTimestamp': 1675441364,
                'timeElapsed': 12,
            }
        },
        {
            'transactionHash': tr_hashes[1],
            'args': {
                'reportTimestamp': 1675441376,
                'timeElapsed': 12,
            }
        },
        {
            'transactionHash': tr_hashes[2],
            'args': {
                'reportTimestamp': 1675441388,
                'timeElapsed': 12,
            }
        },
        {
            'transactionHash': tr_hashes[3],
            'args': {
                'reportTimestamp': 1675441400,
                'timeElapsed': 12,
            }
        },
        {

            'transactionHash': tr_hashes[4],
            'args': {
                'reportTimestamp': 1675441424,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[5],
            'args': {
                'reportTimestamp': 1675441436,
                'timeElapsed': 12,
            }
        },
        {
            'transactionHash': tr_hashes[6],
            'args': {
                'reportTimestamp': 1675441448,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[7],
            'args': {
                'reportTimestamp': 1675441460,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[8],
            'args': {
                'reportTimestamp': 1675441472,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[9],
            'args': {
                'reportTimestamp': 1675441484,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[10],
            'args': {
                'reportTimestamp': 1675441496,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[11],
            'args': {
                'reportTimestamp': 1675441508,
                'timeElapsed': 12,
            }
        }
        ,
        {
            'transactionHash': tr_hashes[12],
            'args': {
                'reportTimestamp': 1675441520,
                'timeElapsed': 12,
            }
        }
    ]


@pytest.mark.unit
def test_group_event_by_transaction_hash(eth_distributed_logs):
    expected = {
        eth_distributed_logs[11]['transactionHash']: eth_distributed_logs[11]['args'],
        eth_distributed_logs[12]['transactionHash']: eth_distributed_logs[12]['args']
    }

    got = Prediction.group_event_by_transaction_hash(eth_distributed_logs, 1675441508)

    assert got == expected


@pytest.mark.unit
def test_get_ETHDistributed_events(eth_distributed_logs):
    lido_contract = MagicMock()
    lido_contract.events.ETHDistributed.get_logs.return_value = eth_distributed_logs

    p = Prediction(lido_contract)
    got = p.get_ETHDistributed_events(ANY, ANY, 1675441508)

    expected = {
        eth_distributed_logs[11]['transactionHash']: eth_distributed_logs[11]['args'],
        eth_distributed_logs[12]['transactionHash']: eth_distributed_logs[12]['args']
    }

    assert got == expected


@pytest.mark.unit
def test_get_TokenRebased_events(token_rebased_logs):
    lido_contract = MagicMock()
    lido_contract.events.TokenRebased.get_logs.return_value = token_rebased_logs

    p = Prediction(lido_contract)
    got = p.get_TokenRebased_events(ANY, ANY, 1675441508)

    expected = {
        token_rebased_logs[11]['transactionHash']: token_rebased_logs[11]['args'],
        token_rebased_logs[12]['transactionHash']: token_rebased_logs[12]['args']
    }

    assert got == expected


@pytest.mark.unit
def test_get_block_interval(token_rebased_logs):
    got_from, got_to = Prediction.get_block_interval(912, 12)
    expected_from = 900
    expected_to = 912

    assert got_from == expected_from
    assert got_to == expected_to


@pytest.mark.unit
@pytest.mark.parametrize(
    "blockstamp, duration_in_slots, slots_per_epoch, seconds_per_slot, percentile_el_rewards_bp, percentile_cl_rewards_bp, expected",
    [
        (
                BlockStamp(block_number=SlotNumber(14),
                           block_timestamp=1675441520),
                13,
                32,
                12,
                5000,
                5000,
                Wei(492799999999999999488)
        ),
        (
                BlockStamp(block_number=SlotNumber(14),
                           block_timestamp=1675441520),
                11,
                32,
                12,
                5000,
                5000,
                Wei(528000000000000000000)
        ),
    ])
def test_get_rewards_per_epoch(blockstamp, duration_in_slots, slots_per_epoch, seconds_per_slot,
                               percentile_el_rewards_bp, percentile_cl_rewards_bp,
                               eth_distributed_logs, token_rebased_logs,
                               expected):
    lido_contract = MagicMock()
    lido_contract.events.ETHDistributed.get_logs.return_value = eth_distributed_logs
    lido_contract.events.TokenRebased.get_logs.return_value = token_rebased_logs

    p = Prediction(lido_contract)
    got = p.get_rewards_per_epoch(
        blockstamp=blockstamp,
        duration_in_slots=duration_in_slots,
        slots_per_epoch=slots_per_epoch,
        seconds_per_slot=seconds_per_slot,
        percentile_el_rewards_bp=percentile_el_rewards_bp,
        percentile_cl_rewards_bp=percentile_cl_rewards_bp,
    )

    assert got == expected


@pytest.mark.unit
@pytest.mark.parametrize("data, basis_point, expected", [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7500, 7.75),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5000, 5.5),
])
def test_percentile(data, basis_point, expected):
    got = Prediction.percentile(data, basis_point)
    assert got == expected
