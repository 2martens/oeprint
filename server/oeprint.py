#!/usr/bin/python3

"""oeprint.py: The main file of the print tool"""

import argparse
import hashlib
import json

__author__ = 'Jim Martens'


def main():
    """Main function for oeprint"""
    parser = argparse.ArgumentParser(description='Printing tool for Orientation Unit')
    parser.add_argument('command', metavar='command', help='the command', choices=['print', 'save'])
    parser.add_argument('data', metavar='data', help='the data for the command')
    arguments = parser.parse_args()

    if arguments['command'] == 'print':
        # do printing stuff
        print_documents(arguments['data'])
    elif arguments['command'] == 'save':
        # do saving stuff
        pass

if __name__ == '__main__':
    main()


def print_documents(data):
    """
    Manages the printing.
    :param data:
    :type data: str
    """
    hash_object = hashlib.sha256(data.encode())
    hash = hash_object.hexdigest()
    hashed_filename = hash + '.pdf'

    try:
        with open('build/' + hashed_filename, 'r', encoding='utf-8') as pdf:
            pass
        # print pdf directly
    except FileNotFoundError:
        # build pdf
        decoded_data = json.loads(data)
        with open('data.json', 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            materials = config_data['materials']
            # determine material files and merge them,save resulting pdf in build dir
