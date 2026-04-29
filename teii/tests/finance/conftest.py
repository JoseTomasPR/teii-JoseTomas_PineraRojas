""" Unit tests for teii.finance subpackage """


import json
import unittest.mock as mock
from importlib import resources

import pandas as pd
from pytest import fixture

import teii.finance.finance


@fixture(scope='session')
def api_key_str():
    return ("nokey")


@fixture(scope='package')
def mocked_requests():
    def mocked_get(url):
        response = mock.Mock()
        response.status_code = 200
        if 'NVDA' in url:
            json_filename = 'TIME_SERIES_WEEKLY_ADJUSTED.NVDA.json'
        else:
            raise ValueError('Ticker no soportado')
        json_resource = resources.files('teii.finance.data').joinpath(json_filename)
        json_data = json.loads(json_resource.read_text(encoding='utf-8'))
        response.json.return_value = json_data
        return response

    # This fixture does not return a value: it patches teii.finance.finance.requests
    # with a local mock to avoid real HTTP calls and keep tests deterministic.
    mocked_requests = mock.Mock()
    mocked_requests.get.side_effect = mocked_get
    teii.finance.finance.requests = mocked_requests


@fixture(scope='package')
def pandas_series_NVDA_prices():
    csv_rsrc = resources.files('teii.finance.data').joinpath('TIME_SERIES_WEEKLY_ADJUSTED.NVDA.aclose.unfiltered.csv')
    with resources.as_file(csv_rsrc) as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['aclose']
    return ds


@fixture(scope='package')
def pandas_series_NVDA_prices_filtered():
    csv_rsrc = resources.files('teii.finance.data').joinpath('TIME_SERIES_WEEKLY_ADJUSTED.NVDA.aclose.filtered.csv')
    with resources.as_file(csv_rsrc) as path2csv:
        df = pd.read_csv(path2csv, index_col=0, parse_dates=True)
        ds = df['aclose']
    return ds
