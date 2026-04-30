"""
Finance Client base class and abstract interface.

Defines :class:`FinanceClient`, the abstract base class that handles
the complete API request lifecycle for all finance data providers.
Concrete subclasses implement the provider-specific URL building,
data-key lookup, and data validation logic.
"""


import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import requests

from teii.finance import (FinanceClientAPIError, FinanceClientInvalidAPIKey,
                          FinanceClientInvalidData, FinanceClientIOError)


class FinanceClient(ABC):
    """Abstract wrapper around a Finance API.

    Handles the complete request lifecycle inside :meth:`__init__`:

    1. Configure the instance logger.
    2. Resolve and validate the API key.
    3. Build and execute the HTTP query via :meth:`_query_api`.
    4. Parse the JSON response via :meth:`_process_query_response`.
    5. Validate the downloaded data via :meth:`_validate_query_data`.

    Concrete subclasses must implement the three abstract methods
    (:meth:`_build_base_query_url_params`, :meth:`_build_query_data_key`,
    :meth:`_validate_query_data`) and call :meth:`_build_data_frame`
    after ``super().__init__()``.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g. ``'NVDA'``).
    api_key : str, optional
        AlphaVantage API key. If *None*, the value of the environment
        variable ``TEII_FINANCE_API_KEY`` is used instead.
    logging_level : int or str, optional
        Python logging level for the internal logger.
        Defaults to ``logging.WARNING``.
    logging_file : str, optional
        Reserved for future use. Currently unused.

    Raises
    ------
    FinanceClientInvalidAPIKey
        If no API key is available after the environment variable
        fallback, or if the key is not a string.
    FinanceClientAPIError
        If the HTTP request to the API fails.
    FinanceClientInvalidData
        If the JSON response is missing expected top-level keys.
    """

    _FinanceBaseQueryURL = "https://www.alphavantage.co/query?"  # Class variable

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING,
                 logging_file: Optional[str] = None) -> None:
        """Initialise the finance client.

        Parameters
        ----------
        ticker : str
            Stock ticker symbol.
        api_key : str, optional
            AlphaVantage API key. Falls back to the ``TEII_FINANCE_API_KEY``
            environment variable when *None*.
        logging_level : int or str, optional
            Python logging level for the internal logger.
        logging_file : str, optional
            Reserved for future use. Currently unused.

        Raises
        ------
        FinanceClientInvalidAPIKey
            If ``api_key`` is *None* after the environment variable lookup,
            or is not a string.
        FinanceClientAPIError
            If the HTTP request to the API fails.
        FinanceClientInvalidData
            If the JSON response is missing expected keys.
        """

        self._ticker: str = ticker
        self._api_key: Optional[str] = api_key

        # Logging configuration
        self._setup_logging(logging_level, logging_file)

        # Finance API key configuration
        self._logger.info("API key configuration")
        if self._api_key is None:
            self._api_key = os.getenv("TEII_FINANCE_API_KEY")
        if self._api_key is None or not isinstance(self._api_key, str):
            raise FinanceClientInvalidAPIKey(f"{self.__class__.__qualname__} operation failed")

        # Query Finance API
        self._logger.info("Finance API access...")
        response = self._query_api()

        # Process query response
        self._logger.info("Finance API query response processing...")
        self._process_query_response(response)

        # Validate query data
        self._logger.info("Finance API query data validation...")
        self._validate_query_data()

        # Panda's Data Frame
        self._data_frame: Optional[pd.DataFrame] = None

    def _setup_logging(self,
                       logging_level: Union[int, str],
                       logging_file: Optional[str]) -> None:
        """Configure the instance logger.

        Parameters
        ----------
        logging_level : int or str
            Python logging level (e.g. ``logging.DEBUG``).
        logging_file : str, optional
            Reserved for future use. Currently unused.
        """

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging_level)

    @classmethod
    def _build_base_query_url(cls) -> str:
        """Return the base query URL shared by all request types.

        Returns
        -------
        str
            AlphaVantage base query URL
            (``'https://www.alphavantage.co/query?'``).
        """

        return cls._FinanceBaseQueryURL

    @abstractmethod
    def _build_base_query_url_params(self) -> str:
        """Return the query-string parameters for this request type.

        Concrete subclasses append provider-specific parameters such as
        the function name, ticker symbol, output size, and API key.

        Returns
        -------
        str
            URL-encoded query-string parameters without a leading ``?``.
        """

        pass  # pragma: nocover

    def _query_api(self) -> requests.Response:
        """Execute the HTTP GET request against the Finance API.

        Returns
        -------
        requests.Response
            Successful HTTP response (status code 200).

        Raises
        ------
        FinanceClientAPIError
            If the HTTP request raises any exception or the status code
            is not 200.
        """

        try:
            url = self.__class__._build_base_query_url()
            params = self._build_base_query_url_params()
            response = requests.get(f"{url}{params}")
            assert response.status_code == 200
        except Exception as e:
            raise FinanceClientAPIError("Unsuccessful API access") from e
        else:
            self._logger.info("Successful API access "
                              f"[URL: {response.url}, status: {response.status_code}]")
        return response

    @classmethod
    def _build_query_metadata_key(cls) -> str:
        """Return the JSON key that holds the response metadata.

        Returns
        -------
        str
            Top-level JSON key for the metadata section
            (``'Meta Data'``).
        """

        return "Meta Data"

    @classmethod
    @abstractmethod
    def _build_query_data_key(cls) -> str:
        """Return the JSON key that holds the time-series data.

        Concrete subclasses return the key specific to the API endpoint
        they wrap (e.g. ``'Weekly Adjusted Time Series'``).

        Returns
        -------
        str
            Top-level JSON key for the data section.
        """

        pass  # pragma: nocover

    def _process_query_response(self, response: requests.Response) -> None:
        """Parse the HTTP response and extract metadata and data payloads.

        Populates ``self._json_metadata`` and ``self._json_data`` from
        the JSON body of *response*.

        Parameters
        ----------
        response : requests.Response
            Successful response returned by :meth:`_query_api`.

        Raises
        ------
        FinanceClientInvalidData
            If the expected top-level JSON keys are absent from the
            response body.
        """

        try:
            json_data_downloaded = response.json()
            self._json_metadata = json_data_downloaded[self._build_query_metadata_key()]
            self._json_data = json_data_downloaded[self._build_query_data_key()]
        except Exception as e:
            self._logger.exception("Error processing query response")
            print(f"Response content: '{response.text}'")
            raise FinanceClientInvalidData("Invalid data") from e
        else:
            self._logger.info("Metadata and data fields found")

        self._logger.info(f"Metadata: '{self._json_metadata}'")
        self._logger.info(f"Data: '{json.dumps(self._json_data)[0:218]}...'")

    @abstractmethod
    def _validate_query_data(self) -> None:
        """Validate the downloaded query data.

        Called after :meth:`_process_query_response`. Concrete subclasses
        verify that ``self._json_metadata`` matches the requested ticker
        or meets any other provider-specific invariants.

        Raises
        ------
        FinanceClientInvalidData
            If the metadata does not satisfy the expected invariants.
        """

        pass  # pragma: nocover

    def to_pandas(self) -> pd.DataFrame:
        """Return the internal data as a :class:`pandas.DataFrame`.

        Returns
        -------
        pandas.DataFrame
            DataFrame indexed by date with one column per data field.
        """

        assert self._data_frame is not None

        return self._data_frame

    def to_csv(self, path2file: Path) -> Path:
        """Write the internal DataFrame to a CSV file.

        Parameters
        ----------
        path2file : pathlib.Path
            Destination file path.

        Returns
        -------
        pathlib.Path
            The same path that was passed in, for easy chaining.

        Raises
        ------
        FinanceClientIOError
            If the file cannot be written due to an :class:`IOError` or
            :class:`PermissionError`.
        """

        assert self._data_frame is not None

        try:
            self._data_frame.to_csv(path2file)
        except (IOError, PermissionError) as e:
            raise FinanceClientIOError(f"Unable to write json data into file '{path2file}'") from e

        return path2file
