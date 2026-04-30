"""
Time Series Finance Client.

Provides :class:`TimeSeriesFinanceClient`, a concrete implementation of
:class:`~teii.finance.FinanceClient` that wraps the AlphaVantage
``TIME_SERIES_WEEKLY_ADJUSTED`` endpoint and exposes weekly price,
volume, dividend, and variation queries as :class:`pandas.Series`.
"""


import datetime as dt
import logging
from typing import Optional, Union

import pandas as pd

from teii.finance import FinanceClient, FinanceClientInvalidData, FinanceClientParamError


class TimeSeriesFinanceClient(FinanceClient):
    """Concrete client for the AlphaVantage TIME_SERIES_WEEKLY_ADJUSTED endpoint.

    Downloads and parses the full weekly-adjusted time series for a single
    ticker symbol and exposes the data through several query methods.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g. ``'NVDA'``).
    api_key : str, optional
        AlphaVantage API key. Falls back to the ``TEII_FINANCE_API_KEY``
        environment variable when *None*.
    logging_level : int or str, optional
        Python logging level for the internal logger.
        Defaults to ``logging.WARNING``.

    Raises
    ------
    FinanceClientInvalidAPIKey
        If no API key is found.
    FinanceClientAPIError
        If the HTTP request to the API fails.
    FinanceClientInvalidData
        If the JSON response is missing or empty, or if the internal
        DataFrame cannot be built from the downloaded data.

    References
    ----------
    .. [1] https://www.alphavantage.co/documentation/
    """

    _data_field2name_type = {
        "1. open":                  ("open",     "float"),
        "2. high":                  ("high",     "float"),
        "3. low":                   ("low",      "float"),
        "4. close":                 ("close",    "float"),
        "5. adjusted close":        ("aclose",   "float"),
        "6. volume":                ("volume",   "int"),
        "7. dividend amount":       ("dividend", "float")
    }

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING) -> None:
        """Initialise and populate the internal DataFrame from the API."""

        super().__init__(ticker, api_key, logging_level)

        self._build_data_frame()

        self._logger.info(f"TimeSeriesFinanceClient initialized for ticker '{ticker}'")

    def _build_data_frame(self) -> None:
        """Build the internal pandas DataFrame from the raw JSON data.

        Converts ``self._json_data`` (a dict of weekly records keyed by
        date string) into a typed :class:`pandas.DataFrame` with a
        :class:`~pandas.DatetimeIndex` sorted in ascending order.

        Raises
        ------
        FinanceClientInvalidData
            If the JSON data section is empty or cannot be converted
            into a valid DataFrame.
        """

        self._logger.debug("Building data frame...")

        try:
            if not self._json_data:
                raise ValueError("No weekly data found in API response")

            # Build Panda's data frame
            data_frame = pd.DataFrame.from_dict(self._json_data, orient='index', dtype='float')

            # Rename data fields
            data_frame = data_frame.rename(columns={key: name_type[0]
                                                    for key, name_type in self._data_field2name_type.items()})

            # Set data field types
            data_frame = data_frame.astype(dtype={name_type[0]: name_type[1]
                                                  for key, name_type in self._data_field2name_type.items()})

            # Set index type
            data_frame.index = data_frame.index.astype("datetime64[ns]")

            # Sort data
            self._data_frame = data_frame.sort_index(ascending=True)

        except Exception as e:
            raise FinanceClientInvalidData("Error building data frame") from e

        self._logger.info(f"Data frame built: {len(self._data_frame)} rows")

    def _build_base_query_url_params(self) -> str:
        """Return query-string parameters for the TIME_SERIES_WEEKLY_ADJUSTED endpoint.

        Returns
        -------
        str
            URL-encoded parameters including function name, ticker symbol,
            output size (``full``), and API key.
        """

        self._logger.debug(f"Building query URL params for ticker '{self._ticker}'")

        return f"function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={self._ticker}&outputsize=full&apikey={self._api_key}"

    @classmethod
    def _build_query_data_key(cls) -> str:
        """Return the JSON key for the weekly-adjusted time-series data section.

        Returns
        -------
        str
            ``'Weekly Adjusted Time Series'``
        """

        logging.getLogger(__name__).debug("Query data key: 'Weekly Adjusted Time Series'")

        return "Weekly Adjusted Time Series"

    def _validate_query_data(self) -> None:
        """Verify that the metadata symbol matches the requested ticker.

        Raises
        ------
        FinanceClientInvalidData
            If the ``'2. Symbol'`` field is absent from the metadata or
            does not match ``self._ticker``.
        """

        try:
            assert self._json_metadata["2. Symbol"] == self._ticker
        except Exception as e:
            raise FinanceClientInvalidData("Metadata field '2. Symbol' not found") from e
        else:
            self._logger.info(f"Metadata key '2. Symbol' = '{self._ticker}' found")

    def weekly_price(self,
                     from_date: Optional[dt.date] = None,
                     to_date: Optional[dt.date] = None) -> pd.Series:
        """Return weekly adjusted close prices, optionally filtered by date range.

        Parameters
        ----------
        from_date : datetime.date, optional
            Start date (inclusive). When both ``from_date`` and
            ``to_date`` are given, only weeks within the interval are
            returned. If either is *None*, no date filtering is applied.
        to_date : datetime.date, optional
            End date (inclusive).

        Returns
        -------
        pandas.Series
            Adjusted close prices indexed by :class:`~pandas.Timestamp`.
            Series name: ``'aclose'``.

        Raises
        ------
        FinanceClientParamError
            If ``from_date > to_date``.
        """

        assert self._data_frame is not None

        self._logger.info(f"Weekly price requested [from_date={from_date}, to_date={to_date}]")

        series = self._data_frame['aclose']

        if from_date is not None and to_date is not None:
            if from_date > to_date:
                raise FinanceClientParamError(
                    f"from_date ({from_date}) must be earlier than or equal to to_date ({to_date})")
            series = series.loc[from_date:to_date]   # type: ignore

        self._logger.info(f"Weekly price returned: {series.count()} records")

        return series

    def weekly_volume(self,
                      from_date: Optional[dt.date] = None,
                      to_date: Optional[dt.date] = None) -> pd.Series:
        """Return weekly trading volume, optionally filtered by date range.

        Parameters
        ----------
        from_date : datetime.date, optional
            Start date (inclusive). When both ``from_date`` and
            ``to_date`` are given, only weeks within the interval are
            returned. If either is *None*, no date filtering is applied.
        to_date : datetime.date, optional
            End date (inclusive).

        Returns
        -------
        pandas.Series
            Weekly trading volumes (integer) indexed by
            :class:`~pandas.Timestamp`. Series name: ``'volume'``.

        Raises
        ------
        FinanceClientParamError
            If ``from_date > to_date``.
        """

        assert self._data_frame is not None

        self._logger.info(f"Weekly volume requested [from_date={from_date}, to_date={to_date}]")

        series = self._data_frame['volume']

        if from_date is not None and to_date is not None:
            if from_date > to_date:
                raise FinanceClientParamError(
                    f"from_date ({from_date}) must be earlier than or equal to to_date ({to_date})")
            series = series.loc[from_date:to_date]   # type: ignore

        self._logger.info(f"Weekly volume returned: {series.count()} records")

        return series

    def highest_weekly_variation(self,
                                 from_date: Optional[dt.date] = None,
                                 to_date: Optional[dt.date] = None) -> tuple[dt.date, float, float, float]:
        """Return the week with the highest intra-week price variation.

        Finds the week that maximises ``high - low`` within the optional
        date range and returns a tuple with the relevant statistics for
        that week.

        Parameters
        ----------
        from_date : datetime.date, optional
            Start date (inclusive). If either bound is *None*, no date
            filtering is applied.
        to_date : datetime.date, optional
            End date (inclusive).

        Returns
        -------
        tuple of (datetime.date, float, float, float)
            A 4-tuple ``(date, high, low, high - low)`` where *date* is
            the week-end date of the maximum-variation week.

        Raises
        ------
        FinanceClientParamError
            If ``from_date > to_date``.
        """

        assert self._data_frame is not None

        self._logger.info(f"Highest weekly variation requested [from_date={from_date}, to_date={to_date}]")

        if from_date is not None and to_date is not None:
            if from_date > to_date:
                raise FinanceClientParamError(
                    f"from_date ({from_date}) must be earlier than or equal to to_date ({to_date})")
            df = self._data_frame.loc[from_date:to_date]   # type: ignore
        else:
            df = self._data_frame

        variation = df['high'] - df['low']
        idx = variation.idxmax()

        result = (idx.date(), float(df.loc[idx, 'high']), float(df.loc[idx, 'low']), float(variation.loc[idx]))

        self._logger.info(f"Highest weekly variation: date={result[0]}, high-low={result[3]:.4f}")

        return result

    def yearly_dividends(self,
                         from_year: Optional[int] = None,
                         to_year: Optional[int] = None) -> pd.Series:
        """Return total annual dividends per year, optionally filtered by year range.

        Sums all weekly dividend amounts for each calendar year within
        the optional year range.

        Parameters
        ----------
        from_year : int, optional
            First year (inclusive). When both ``from_year`` and
            ``to_year`` are given, only years within the interval are
            summed. If either is *None*, no year filtering is applied.
        to_year : int, optional
            Last year (inclusive).

        Returns
        -------
        pandas.Series
            Annual dividend totals (float) indexed by calendar year
            (int). Series name: ``'dividend'``.

        Raises
        ------
        FinanceClientParamError
            If ``from_year > to_year``.
        """

        assert self._data_frame is not None

        self._logger.info(f"Yearly dividends requested [from_year={from_year}, to_year={to_year}]")

        series = self._data_frame['dividend']

        if from_year is not None and to_year is not None:
            if from_year > to_year:
                raise FinanceClientParamError(
                    f"from_year ({from_year}) must be earlier than or equal to to_year ({to_year})")
            series = series[(series.index.year >= from_year) & (series.index.year <= to_year)]

        result = series.groupby(series.index.year).sum()

        self._logger.info(f"Yearly dividends returned: {result.count()} years")

        return result
