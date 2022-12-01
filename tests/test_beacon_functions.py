import pytest
import json

from requests import Session

from app.review.beacon import BeaconChainClient

with open('tests/responses.json', 'r') as file:
    responses = json.load(file)

# fmt: off
key_list = [
    b"\xa3\x84\xf0\xd7w\x1d\xe0'\x8e\x0e\x9b\x13$\xb1\xa0\x9b\xb8\xb3\xf8\xa6-\xff\xcd\xb87\x06\xe38vM\xe8\x93\xc6H\xd6\xab\xdbN\x02^\xf0\xe8ZQ\x1aw\xa2.", # noqa E501
    b'\x91\x84Z\x12\xe0\x7fW\xbd\x1c\xa8\xba\x87\xc2\x97F\x1c u\xc7l\xe6\x00\xb9\xbb\x88\x99\xde\x00\x88\xf0\x92y\xee^R+\x84u\x9f\x1a\x85|J\x9a\x04\x8a5\x8b', # noqa E501
    b'\x81\xcc\xb4\xd16\xcc&\x13\xad*\xce7#\xac\xd5\xaaD\xf6\xb2r\xe2\x10\xe0\x08tN\xfb\xb2Oh\xe4\xbfaB\x7f\x07\xdb\x99\xdd\xc6\x87F\x10\xd7\xe5\x13\x08h', # noqa E501
    b'\xb8\xcd\x03\xfap-\xddG\xb8&\xa3P\x86Q\xe8@f_\x18h\xb3\x8cEp\x93\xcb\xcbi\x05\xf5\xa80P\xe3\x1b\x84p*\x9f\x19\x10\xc6\xff\xdf\x90\xad\xeb\x16' # noqa E501
]


# fmt: on


class MockResponse:
    def __init__(self, json):
        self.json_text = json
        self.text = json

    def json(self):
        return json.loads(self.json_text)


@pytest.fixture
def lighthouse_requests(monkeypatch):
    version = json.dumps(responses['lighthouse']['version'])
    genesis = json.dumps(responses['lighthouse']['genesis'])
    finalized_epoch = json.dumps(responses['lighthouse']['finalized_epoch'])
    head_actual = json.dumps(responses['lighthouse']['head_actual'])
    head_finalized = json.dumps(responses['lighthouse']['head_finalized'])
    validators = json.dumps(responses['lighthouse']['validators'])

    def mocked_get(self, uri, *args, **kwargs):
        """A method replacing Requests.get
        Returns a mocked response object (with json method)
        """
        if 'eth/v1/node/version' in uri:
            return MockResponse(version)
        if 'eth/v1/beacon/genesis' in uri:
            return MockResponse(genesis)
        if 'eth/v1/beacon/states/head/finality_checkpoints' in uri:
            return MockResponse(finalized_epoch)
        if 'eth/v1/beacon/headers/head' in uri:
            return MockResponse(head_actual)
        if 'eth/v1/beacon/headers/finalized' in uri:
            return MockResponse(head_finalized)
        if 'validators' in uri:
            return MockResponse(validators)
        else:
            return MockResponse('')

    # finally, patch requests.get and requests.post with patched version
    monkeypatch.setattr(Session, 'get', mocked_get)
    monkeypatch.setattr(Session, 'post', mocked_get)


@pytest.fixture
def bad_requests(monkeypatch):
    version = 'Mock'

    def mocked_get(self, uri, *args, **kwargs):
        """A method replacing Requests.get
        Returns a mocked response object (with json method)
        """
        return MockResponse(version)

    # finally, patch requests.get and requests.post with patched version
    monkeypatch.setattr(Session, 'get', mocked_get)
    monkeypatch.setattr(Session, 'post', mocked_get)


def test_finalized_epoch(lighthouse_requests):
    beacon = BeaconChainClient('localhost', 1)
    result = beacon.get_finalized_epoch()
    assert result == 23714


def test_balance(lighthouse_requests):
    beacon = BeaconChainClient('localhost', 1)
    result = beacon.get_balances(10, key_list)
    assert result == (445738262310000000000, 4, 221738262310000000000)
