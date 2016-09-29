

import json

import pytest

from srjson import srjson, SRJSON


def hasher(d):

    return hash(json.dumps(d, sort_keys=True))


def test_simple(simple):

    expected = {
        'a': 'foo/bar',
        'b': 'foo'
    }

    result = srjson.loads(simple)

    assert hasher(result) == hasher(expected)


def test_array(array):

    expected = [
        {
            'a': 'foo/bar',
            'b': 'foo'
        },
        {
            'a': 'qux/baz',
            'b': 'qux'
        }
    ]

    result = srjson.loads(array)

    assert hasher(result) == hasher(expected)


def test_kitchen_sink(kitchen_sink):

    expected = {
        "kind": "prod",
        "repos": {
            "services": "/repos/prod_services",
            "apps": "/repos/prod_apps",
            "ui": "/repos/ui",
            "root": "/repos",
            "server": "/repos/prod_server"
        },
        "apps_to": "foo/server/apps",
        "services_to": "foo/server/services",
        "to": "foo",
        "clones": [
            {
                "to": "foo",
                "from": "/repos/prod_server",
                "name": "server"
            },
            {
                "to": "foo/server/services/auth",
                "from": "/repos/prod_services/auth",
                "name": "auth"
            },
            {
                "to": "foo/server/apps/number_cruncher",
                "from": "/repos/prod_apps/number_cruncher",
                "name": "number_cruncher"
            },
            {
                "to": "foo/server/apps/number_cruncher/frontend/ui",
                "from": "/repos/ui",
                "name": "ui"
            }
        ]
    }

    memo = {
        'to': 'foo'
    }

    result = srjson.loads(kitchen_sink, memo=memo)

    assert hasher(result) == hasher(expected)


@pytest.mark.skip(reason="TODO: cyclical structures hit max recursion")
def test_cyclical(cyclical):

    expected = {}

    result = srjson.loads(cyclical)

    assert hasher(result) == hasher(expected)


def test_custom_delimiters(percent_delimiters):

    _srjson = SRJSON(delimiters=('%', '%'))

    expected = {
        'a': 'foo/bar',
        'b': 'foo'
    }

    result = _srjson.loads(percent_delimiters)

    assert hasher(result) == hasher(expected)


def test_custom_delimiters_via_loads(percent_delimiters):

    expected = {
        'a': 'foo/bar',
        'b': 'foo'
    }

    result = srjson.loads(percent_delimiters, delimiters=('%', '%'))

    assert hasher(result) == hasher(expected)
