#!/usr/bin/env python2.7

"""
This script will generate a dynamicItemAttributes.json file using res files
"""


import argparse
import os
import re
import sqlite3
import json

from PIL import Image

from shutil import copyfile

parser = argparse.ArgumentParser(description='This script updates module icons for pyfa')
parser.add_argument('-e', '--eve', required=True, type=str, help='path to eve\'s ')
parser.add_argument('-s', '--server', required=False, default='tq', type=str, help='which server to use (defaults to tq)')
args = parser.parse_args()

LOADER_FILE = 'app:/bin/dynamicItemAttributesLoader.pyd'
RES_FILE = 'res:/staticdata/dynamicitemattributes.fsdbinary'

binaryfile = os.path.split(RES_FILE)[1]

eve_path = os.path.join(args.eve, 'index_{}.txt'.format(args.server))
with open(eve_path, 'r') as f:
    lines = f.readlines()
    file_index = {x.split(',')[0]: x.split(',') for x in lines}

resfileindex = file_index['app:/resfileindex.txt']

res_cache = os.path.join(args.eve, 'ResFiles')

with open(os.path.join(res_cache, resfileindex[1]), 'r') as f:
    lines = f.readlines()
    res_index = {x.split(',')[0].lower(): x.split(',') for x in lines}

# Need to copy the file to  our cuirrent directory
attribute_loader_file = os.path.join(res_cache, file_index[LOADER_FILE][1])
to_path = os.path.dirname(os.path.abspath(__file__))
copyfile(attribute_loader_file, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.split(LOADER_FILE)[1]))

# The loader expect it to be the correct filename, so copy trhe file as well
dynattribute_file = os.path.join(res_cache, res_index[RES_FILE.lower()][1])
to_path = os.path.dirname(os.path.abspath(__file__))
copyfile(dynattribute_file, os.path.join(os.path.dirname(os.path.abspath(__file__)), binaryfile))

import dynamicItemAttributesLoader

attributes = dynamicItemAttributesLoader.load(os.path.join(to_path, binaryfile))

attributes_obj = {}

# convert top level to dict
attributes = dict(attributes)

# This is such a brute force method. todo: recursively generate this by inspecting the objects
for k, v in attributes.items():
    attributes_obj[k] = {
        'attributeIDs': dict(v.attributeIDs),
        'inputOutputMapping': list(v.inputOutputMapping)
    }

    for i, x in enumerate(v.inputOutputMapping):
        attributes_obj[k]['inputOutputMapping'][i] = {
            'resultingType': x.resultingType,
            'applicableTypes': list(x.applicableTypes)
        }

    for k2, v2 in v.attributeIDs.items():
        attributes_obj[k]['attributeIDs'][k2] = {
            'min': v2.min,
            'max': v2.max
        }

with open('dynamicattributes.json', 'w') as outfile:
    json.dump(attributes_obj, outfile)
