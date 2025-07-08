class PhoneBookError(Exception):
    """Base class for phone book exceptions."""

    pass


class FileNotOpenedError(PhoneBookError):
    """Raised when trying to perform operations before opening the phone book file."""

    def __str__(self):
        return "Phone book file is not opened. Please open the file first."


class TryOpenFileError(PhoneBookError):
    """Raised when trying to open a file that is already opened."""

    def __str__(self):
        return "Phone book is already opened. Close it before opening again."


class IncorrectPhoneNumberDigit(PhoneBookError):
    """Raised when a phone number exceeds the maximum allowed digits."""

    def __str__(self):
        return "Phone number should not exceed 11 digits."


class InvalidPhoneNumberLatter(PhoneBookError):
    """Raised when a phone number contains non-digit characters."""

    def __str__(self):
        return "Phone number should contain only digits."
