"""
Custom exceptions for runpandas
"""


class InvalidFileError(Exception):
    def __init__(self, msg):
        message = "It doesn't like a valid  %s file!" % (msg)
        super().__init__(message)


class RequiredColumnError(Exception):
    def __init__(self, column, cls=None):
        if cls is None:
            message = "{!r} column not found".format(column)
        else:
            message = "{!r} column should be of type {!s}".format(column, cls)
        super().__init__(message)
