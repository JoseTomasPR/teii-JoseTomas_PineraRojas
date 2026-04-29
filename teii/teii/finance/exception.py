""" Exception classes """


class FinanceClientError(Exception):
    """FinanceClient exception base class.

    https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/ (Transformer Pattern)
    """

    pass


class FinanceClientInvalidAPIKey(FinanceClientError):
    """
    Invalid finance API Key.
    """

    pass


class FinanceClientAPIError(FinanceClientError):
    """
    Finance API access failure.
    """

    pass


class FinanceClientInvalidData(FinanceClientError):
    """
    Finance API returned incomplete or malformed data.
    """

    pass


class FinanceClientIOError(FinanceClientError):
    """
    Error reading or writing data file.
    """

    pass
