"""
teii.finance - Finance client subpackage.

Wraps the AlphaVantage REST API to expose weekly-adjusted time-series
financial data as :class:`pandas.Series` objects. All public symbols
are re-exported from this namespace so that consumers need only import
from ``teii.finance``.

Classes
-------
FinanceClient
    Abstract base class that handles the full API request lifecycle:
    URL building, HTTP query, response parsing, and data validation.
TimeSeriesFinanceClient
    Concrete client for the ``TIME_SERIES_WEEKLY_ADJUSTED`` endpoint.
    Exposes weekly price, volume, dividend, and variation queries.

Exceptions
----------
FinanceClientError
    Base class for all exceptions raised by this package.
FinanceClientInvalidAPIKey
    Raised when the API key is missing or not a string.
FinanceClientAPIError
    Raised when the HTTP request to the AlphaVantage API fails.
FinanceClientInvalidData
    Raised when the API response contains incomplete or malformed data.
FinanceClientParamError
    Raised when an invalid parameter is supplied to a client method.
FinanceClientIOError
    Raised when a file read/write operation fails.
"""


from .exception import (FinanceClientAPIError, FinanceClientInvalidAPIKey,
                        FinanceClientInvalidData, FinanceClientIOError,
                        FinanceClientParamError)
from .finance import FinanceClient
from .timeseries import TimeSeriesFinanceClient

__all__ = ('FinanceClientInvalidAPIKey',
           'FinanceClientAPIError',
           'FinanceClientInvalidData',
           'FinanceClientIOError',
           'FinanceClientParamError',
           'FinanceClient',
           'TimeSeriesFinanceClient')
