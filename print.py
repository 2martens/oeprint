"""print.py; Provides functionality for printing"""

__author__ = 'Jim Martens'

from subprocess import call


def print_files(printer, files):
    """
    Prints the given files on the given printer.
    :type printer: str
    :type files: list
    """
    for file in files:
        call(['lpr', '-o fitplot', '-o fit-to-page', file['options'], '-U oe', '-P' + printer, '-# ' + str(file['prints']),
              file['path']])
