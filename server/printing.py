"""printing.py; Provides functionality for printing"""

__author__ = 'Jim Martens'

from subprocess import call


def print_files(printer, files):
    """
    Prints the given files on the given printer.
    :type printer: str
    :type files: list
    """
    for file in files:
        options = ['-o fitplot', '-o fit-to-page']
        options += file['options'] if file['options'] else []
        call(['lpr'] + options + ['-U oe', '-P' + printer, '-# ' + str(file['prints']), file['path']])


def print_merged_file(printer, merge_file):
    """
    Prints the given merged PDF file on the given printer.
    :param printer: str
    :param merge_file: str
    """
    call(['lpr', '-o fitplot', '-o fit-to-page', '-U oe', '-P' + printer, '-#1', merge_file])
