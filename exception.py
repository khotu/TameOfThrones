class Error(Exception):
    """Base class for other exceptions"""
    pass


class KingdomNotFound(Error):
    """Exception raised when Kingdom is not found."""
    def __str__(self):
        return "Kindom not Found. Are you sure you are in correct planet?"

class CompetitiorFound(Error):
    """Exception raised when competitior is found ."""
    def __str__(self):
        return "competitior Found."

class InvalidAllyKingdom(Error):
    """Exception raised when Ally Kingdom is not valid."""
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class InvalidMessageException(Error):
    """Exception raised when Invalid Message is sent."""
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message



class InputFileError(Error):
    """Exception raised when Input File is not found"""
    def __str__(self):
        return "Message File not Found. Are you sure you gave the path for input message file?"