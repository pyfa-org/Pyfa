"""
Script used to extract values from section-less configs.

Used in linux image build process.
"""

import argparse
import configparser
import os


parser = argparse.ArgumentParser(description='Extract values from section-less configs')
parser.add_argument('path', help='path to config file')
parser.add_argument('variable', help='variable name')
args = parser.parse_args()

with open(os.path.expanduser(args.path), 'r') as file:
    text = file.read()

config = configparser.ConfigParser()
config.read_string(f'[root]\n{text}')
print(config.get('root', args.variable))
