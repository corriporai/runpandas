"""
Custom exceptions for runpandas
"""


class InvalidFileError(Exception):
    def __init__(self, format):
        message = "It doesn't like a valid  %s file!" % (format)
        super().__init__(message)
