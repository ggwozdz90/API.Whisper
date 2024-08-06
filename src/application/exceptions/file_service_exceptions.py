class FileServiceException(Exception):
    """Base exception for file service errors."""

    pass


class FileSaveException(FileServiceException):
    """Exception raised when a file cannot be saved."""

    pass


class FileDeleteException(FileServiceException):
    """Exception raised when a file cannot be deleted."""

    pass
