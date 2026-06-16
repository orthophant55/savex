class KboIngestionError(Exception):
    """Base exception for KBO ingestion errors."""


class KboDataClientError(KboIngestionError):
    """Raised when kbodata package call fails."""


class KboDataUnavailableError(KboIngestionError):
    """Raised when kbodata package is not installed."""


class ChromeDriverNotFoundError(KboIngestionError):
    """Raised when ChromeDriver path is missing or invalid."""


class KboDataParseError(KboIngestionError):
    """Raised when raw kbo-data payload cannot be parsed."""
