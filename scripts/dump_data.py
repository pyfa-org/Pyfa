#!/usr/bin/env python
"""
This script bootstraps Phobos from a supplied path and feeds it
information regarding EVE data paths and where to dump data. It then imports
some other scripts and uses them to convert the json data into a SQLite
database and then compare the new database to the existing one, producing a
diff which can then be used to assist in the updating.
"""

import sys
import os
import json
import re
import natsort
from collections import OrderedDict

from itertools import izip_longest

try:
    major = sys.version_info.major
    minor = sys.version_info.minor
except AttributeError:
    major = sys.version_info[0]
    minor = sys.version_info[1]
if major != 2 or minor < 7:
    sys.stderr.write('This application requires Python 2.7 to run, but {0}.{1} was used\n'.format(major, minor))
    sys.exit()

import argparse
import os.path

parser = argparse.ArgumentParser(description='This script extracts data from EVE client and writes it into JSON files')
parser.add_argument(
    '-e', '--eve', required=True, help='Path to EVE client\'s folder')
parser.add_argument(
    '-p', '--phobos', required=True, help="Location of Phobos")
parser.add_argument(
    '-s', '--server', default='tq', help='Server to pull data from. Default is "tq"',
    choices=('tq', 'sisi', 'duality', 'thunderdome', 'serenity'))
parser.add_argument(
    '-j', '--json', required=True, help='Output folder for the JSON files')
parser.add_argument(
    '-t', '--translate', default='multi',
    help='Attempt to translate strings into specified language. Default is "multi"',
    choices=('de', 'en-us', 'es', 'fr', 'it', 'ja', 'ru', 'zh', 'multi'))

args = parser.parse_args()

# Expand home directory
path_eve = os.path.expanduser(args.eve)
path_json = os.path.expanduser(args.json)

sys.path.append(os.path.expanduser(args.phobos))

from flow import FlowManager
from miner import *
from writer import *
from util import ResourceBrowser, Translator
from writer.base import BaseWriter
from writer.json_writer import CustomEncoder


class PyfaJsonWriter(BaseWriter):
    """
    Class, which stores fetched data on storage device
    as JSON files.
    """

    def __init__(self, folder, indent=None, group=None):
        self.base_folder = folder
        self.indent = indent
        self.group = group

    @staticmethod
    def __grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    def write(self, miner_name, container_name, container_data):
        # Create folder structure to path, if not created yet
        folder = os.path.join(self.base_folder, self.__secure_name(miner_name))
        if not os.path.exists(folder):
            os.makedirs(folder, mode=0o755)

        if type(container_data) == dict:
            container_data = OrderedDict(natsort.natsorted(container_data.items()))

        if self.group is None:
            filepath = os.path.join(folder, u'{}.json'.format(self.__secure_name(container_name)))
            self.__write_file(container_data, filepath)
        else:
            for i, group in enumerate(PyfaJsonWriter.__grouper(container_data, self.group)):
                filepath = os.path.join(folder, u'{}.{}.json'.format(self.__secure_name(container_name), i))
                if type(container_data) in (dict, OrderedDict):
                    data = dict((k, container_data[k]) for k in group if k is not None)
                else:
                    data = [k for k in group if k is not None]
                self.__write_file(data, filepath)

    def __write_file(self, data, filepath):
        data_str = json.dumps(
            data,
            ensure_ascii=False,
            cls=CustomEncoder,
            indent=self.indent,
            # We're handling sorting in customized encoder
            sort_keys=False)
        data_bytes = data_str.encode('utf8')
        with open(filepath, 'wb') as f:
            f.write(data_bytes)

    def __secure_name(self, name):
        """
        As we're writing to disk, we should get rid of all
        filesystem-specific symbols.
        """
        # Prefer safe way - replace any characters besides
        # alphanumeric and few special characters with
        # underscore
        writer_safe_name = re.sub('[^\w\-.,() ]', '_', name, flags=re.UNICODE)
        return writer_safe_name


path_eve=path_eve
server_alias=args.server
language=args.translate
path_json=path_json

resource_browser = ResourceBrowser(eve_path=path_eve, server_alias=server_alias)

pickle_miner = PickleMiner(resbrowser=resource_browser)
trans = Translator(pickle_miner=pickle_miner)
fsdlite_miner = FsdLiteMiner(resbrowser=resource_browser, translator=trans)
fsdbinary_miner = FsdBinaryMiner(resbrowser=resource_browser, translator=trans)
miners = [
    MetadataMiner(resbrowser=resource_browser),
    fsdlite_miner,
    fsdbinary_miner,
    TraitMiner(fsdlite_miner=fsdlite_miner, fsdbinary_miner=fsdbinary_miner, translator=trans),
    pickle_miner]

writers = [
    PyfaJsonWriter(path_json, indent=2, group=5000)]

filters = 'dogmaattributes,dogmaeffects,dogmaunits,dynamicitemattributes,marketgroups,metagroups,' \
          'typedogma,requiredskillsfortypes,clonegrades,dbuffcollections,evecategories,evegroups,' \
          'evetypes,traits,metadata'

FlowManager(miners, writers).run(filter_string=filters, language=language)
