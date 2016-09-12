#!/usr/bin/python3

"""oeprint.py: The main file of the print tool"""

import argparse
import hashlib
import json
import os

from tool.merge import merge_pdf_files
from tool.printing import print_merged_file

__author__ = 'Jim Martens'


def main():
    """Main function for oeprint"""
    parser = argparse.ArgumentParser(description='Printing tool for Orientation Unit')
    parser.add_argument('command', metavar='command', help='the command', choices=['print', 'save', 'debug'])
    parser.add_argument('data', metavar='data', help='the data for the command')
    arguments = parser.parse_args()

    if arguments.command == 'print':
        # do printing stuff
        print_documents(arguments.data)
    elif arguments.command == 'save':
        # do saving stuff
        pass
    elif arguments.command == 'debug':
        print(arguments.data)


def print_documents(data):
    """
    Manages the printing.
    :param data:
    :type data: str
    """
    hash_object = hashlib.sha256(data.encode())
    hash_str = hash_object.hexdigest()
    hashed_filename = hash_str + '.pdf'
    decoded_data = json.loads(data)

    try:
        filename = 'build/' + hashed_filename
        with open(filename, 'r', encoding='utf-8'):
            pass
        modification_time = os.path.getmtime(filename)
        with open('data.json', 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            materials = config_data['materials']
            for material in materials:
                if material['name'] not in decoded_data['amounts']:
                    continue
                current_modification_time = os.path.getmtime(material['filename'])
                if current_modification_time > modification_time:
                    build_merged_pdf(hashed_filename, decoded_data)
                    break
        print_merged_file(decoded_data['printer'], 'build/' + hashed_filename)
    except FileNotFoundError:
        # build pdf
        build_merged_pdf(hashed_filename, decoded_data)
        print_merged_file(decoded_data['printer'], 'build/' + hashed_filename)


def build_merged_pdf(filename, data):
    with open('data.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        materials = config_data['materials']
        processed_materials = process_materials(materials)
        print_amounts = data['amounts']
        
        merge_data = []
        for material_name in print_amounts:
            material = processed_materials[material_name]
            amount = print_amounts[material_name]
            merge_data.append({
                'material': material,
                'amount': amount
            })
        
        merge_pdf_files('build/' + filename, merge_data)


def process_materials(materials):
    processed_materials = {}
    for material in materials:
        processed_materials[material['name']] = material
        children = material['children']
        if children:
            sub_materials = process_materials(children)
            processed_materials.update(sub_materials)

    return processed_materials


if __name__ == '__main__':
    main()
