#!/usr/bin/python3

"""oeprint.py: The main file of the print tool"""

__author__ = 'Jim Martens'

import argparse
import sys

from config import Config
from file import *
from print import *


def main():
    """Main function for oeprint"""
    year = '2015'

    parser = argparse.ArgumentParser(description='Printing tool for Orientation Unit')
    parser.add_argument('build', metavar='build', help='the identifier of the build')
    parser.add_argument('prints', metavar='numberOfPrints', type=int, help='how often the build is printed')
    parser.add_argument('--printer', dest='printer', help='a valid printer name like d116_sw', default='e120_hp')
    arguments = parser.parse_args()
    config = Config('configuration/config.json')
    build_data = config.load_build(arguments.build)
    if build_data:
        build_data['files'] = insert_file_paths(year, 'files', build_data['files'])
        for i in range(0, arguments.prints):
            if build_data['files']:
                print_files(arguments.printer, build_data['files'])
            if build_data['builds']:
                print_builds(config, year, arguments.printer, build_data['builds'])

    else:
        print('Invalid build', file=sys.stderr)

if __name__ == '__main__':
    main()


def print_builds(config, year, printer, builds):
    """
    Prints builds
    :type config: config.Config
    :type year: str
    :type printer: str
    :type builds: list
    """
    for build in builds:
        build_data = config.load_build(build)
        build_data['files'] = insert_file_paths(year, 'files', build_data['files'])
        print_files(printer, build_data['files'])
