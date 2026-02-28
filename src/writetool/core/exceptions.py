"""Custom exceptions for WriteTool."""


class WriteToolError(Exception):
    """Base exception for all WriteTool errors."""


class ISOError(WriteToolError):
    """Error related to ISO file operations."""


class ISONotFoundError(ISOError):
    """ISO file does not exist."""


class InvalidISOError(ISOError):
    """File is not a valid ISO image."""


class DriveError(WriteToolError):
    """Error related to drive operations."""


class DriveNotFoundError(DriveError):
    """Target drive not found or disconnected."""


class DriveInUseError(DriveError):
    """Target drive is mounted and could not be unmounted."""


class FormatError(DriveError):
    """Error during drive formatting."""


class WriteError(WriteToolError):
    """Error during file writing."""


class WriteCancelledError(WriteError):
    """Write operation was cancelled by user."""


class ChecksumError(WriteToolError):
    """Checksum mismatch."""


class WimError(WriteToolError):
    """Error related to WIM operations."""


class WimlibNotFoundError(WimError):
    """wimlib-imagex is not installed."""


class PrivilegeError(WriteToolError):
    """Insufficient privileges for the operation."""


class PlatformNotSupportedError(WriteToolError):
    """Current platform is not supported."""
