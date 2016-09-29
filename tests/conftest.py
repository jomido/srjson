
import pytest


@pytest.fixture(scope='module')
def simple():

    with open('tests/fixtures/simple.srjson', 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def array():

    with open('tests/fixtures/array.srjson', 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def kitchen_sink():

    with open('tests/fixtures/kitchen_sink.srjson', 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def cyclical():

    with open('tests/fixtures/cyclical.srjson', 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def percent_delimiters():

    with open('tests/fixtures/percent_delimiters.srjson', 'r') as f:
        return f.read()

