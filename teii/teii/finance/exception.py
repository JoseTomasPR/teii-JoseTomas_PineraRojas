"""
Exception classes for the teii.finance package.

Defines the exception hierarchy used throughout the package. All
exceptions derive from :class:`FinanceClientError` so that callers can
choose to catch the full family with a single ``except`` clause.
"""


class FinanceClientError(Exception):
    """Base exception class for all teii.finance errors.

    All exceptions raised by this package derive from this class,
    following the Transformer Pattern for exception chaining.

    References
    ----------
    .. [1] https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/
    """

    pass


class FinanceClientInvalidAPIKey(FinanceClientError):
    """Raised when the AlphaVantage API key is missing or invalid.

    Raised in :meth:`~teii.finance.FinanceClient.__init__` when no API
    key is provided as a constructor argument or via the environment
    variable ``TEII_FINANCE_API_KEY``, or when the key is not a string.
    """

    pass


class FinanceClientAPIError(FinanceClientError):
    """Raised when the HTTP request to the AlphaVantage API fails.

    Wraps any :class:`requests.exceptions.RequestException` raised
    during the API query so callers can catch a single package-specific
    exception type.
    """

    pass


class FinanceClientInvalidData(FinanceClientError):
    """Raised when the API response contains incomplete or malformed data.

    Raised when the JSON response is missing expected top-level keys,
    when the weekly data section is empty, or when the internal
    DataFrame cannot be constructed from the downloaded data.
    """

    pass


class FinanceClientParamError(FinanceClientError):
    """Raised when an invalid parameter is passed to a client method.

    Typically raised when a date or year interval is inverted, i.e.
    ``from_date > to_date`` or ``from_year > to_year``.
    """

    pass


class FinanceClientIOError(FinanceClientError):
    """Raised when a file read/write operation fails.

    Wraps :class:`IOError` and :class:`PermissionError` that may be
    raised by :meth:`~teii.finance.FinanceClient.to_csv`.
    """

    pass
