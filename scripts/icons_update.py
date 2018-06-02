#!/usr/bin/env python2.7

"""
This script updates only market/item icons.
"""


import argparse
import os
import re
import sqlite3

from PIL import Image
from shutil import copyfile

parser = argparse.ArgumentParser(description='This script updates module icons for pyfa')
parser.add_argument('-e', '--eve', required=True, type=str, help='path to eve\'s ')
parser.add_argument('-s', '--server', required=False, default='tq', type=str, help='which server to us (defaults to tq)')
parser.add_argument('-i', '--icons', required=True, type=str, help='Path to icons .json')
args = parser.parse_args()


script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(script_dir, '..', 'eve.db'))
icons_dir = os.path.abspath(os.path.join(script_dir, '..', 'imgs', 'icons'))
export_dir = os.path.abspath(os.path.expanduser(os.path.join(args.icons, 'items')))

dirs = [export_dir, os.path.join(export_dir, "Modules")]

db = sqlite3.connect(db_path)
cursor = db.cursor()

ICON_SIZE = (16, 16)

ITEM_CATEGORIES = (
    2,  # Celestial
    6,  # Ship
    7,  # Module
    8,  # Charge
    16,  # Skill
    18,  # Drone
    20,  # Implant
    32,  # Subsystem
    66,  # Structure Module
)

MARKET_ROOTS = {
    9,  # Modules
    1111,  # Rigs
    157,  # Drones
    11,  # Ammo
    1112,  # Subsystems
    24,  # Implants & Boosters
    404,  # Deployables
    2202,  # Structure Equipment
    2203  # Structure Modifications (Rigs)
}

# todo: figure out how icons work
loaders = {
    "app:/bin/graphicIDsLoader.pyd": "res:/staticdata/graphicIDs.fsdbinary",
}

import json
with open(args.icons, 'r') as f:
    icon_json = json.load(f)

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
graphics_loader_file = os.path.join(res_cache, file_index['app:/bin/graphicIDsLoader.pyd'][1])
to_path = os.path.dirname(os.path.abspath(__file__))
copyfile(graphics_loader_file, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphicIDsLoader.pyd'))

# The loader expect it to be the correct filename, so copy trhe file as well
graphics_file = os.path.join(res_cache, res_index['res:/staticdata/graphicIDs.fsdbinary'.lower()][1])
to_path = os.path.dirname(os.path.abspath(__file__))
copyfile(graphics_file, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphicIDs.fsdbinary'))

import graphicIDsLoader

print(dir(graphicIDsLoader))

graphics = graphicIDsLoader.load(os.path.join(to_path, 'graphicIDs.fsdbinary'))

graphics_py_ob = {}
for x, v in graphics.items():
    if (hasattr(v, 'iconFolder')):
        graphics_py_ob[x] = v.iconFolder

# Add children to market group list
# {parent: {children}}
mkt_tree = {}
for row in cursor.execute('select marketGroupID, parentGroupID from invmarketgroups'):
    parent = row[1]
    # We have all the root groups in the set we need anyway
    if not parent:
        continue
    child = row[0]
    children = mkt_tree.setdefault(parent, set())
    children.add(child)

# Traverse the tree we just composed to add all children for all needed roots
def get_children(parent):
    children = set()
    for child in mkt_tree.get(parent, ()):
        children.add(child)
        children.update(get_children(child))
    return children


market_groups = set()
for root in MARKET_ROOTS:
    market_groups.add(root)
    market_groups.update(get_children(root))


query_items = 'select distinct iconID from invtypes'
query_groups = 'select distinct iconID from invgroups'
query_cats = 'select distinct iconID from invcategories'
query_market = 'select distinct iconID from invmarketgroups'
query_attrib = 'select distinct iconID from dgmattribs'

needed = set()
existing = set()
export = {}


# Get a list of needed icons based on the items / attributes / etc from the database
for query in (query_items, query_groups, query_cats, query_market, query_attrib):
    for row in cursor.execute(query):
        fname = row[0]
        if fname is None:
            continue
        needed.add(fname)

# Get a list of all the icons we currently have
for fname in os.listdir(icons_dir):
    if not os.path.isfile(os.path.join(icons_dir, fname)):
        continue
    fname = os.path.splitext(fname)[0]
    # Get rid of "icon" prefix as well
    #fname = re.sub('^icon', '', fname)
    print(fname,"exists")
    existing.add(fname)

def crop_image(img):
    w, h = img.size
    if h == w:
        return img
    normal = min(h, w)
    diff_w = w - normal
    diff_h = h - normal
    crop_top = diff_h // 2
    crop_bot = diff_h // 2 + diff_h % 2
    crop_left = diff_w // 2
    crop_right = diff_w // 2 + diff_w % 2
    box = (crop_left, crop_top, w - crop_right, h - crop_bot)
    return img.crop(box)


def get_icon_file(request):
    """
    Get the iconFile field value and find proper
    icon for it. Return as PIL image object down-
    scaled for use in pyfa.
    """

    # the the res file
    icon = icon_json[str(request)]
    key = icon['iconFile'].lower()
    if key not in res_index:
        return None
    res_icon = res_index[key]
    icon_path = res_icon[1]

    fullpath = os.path.join(res_cache, icon_path)

    if not os.path.isfile(fullpath):
        return None
    img = Image.open(fullpath)
    img = crop_image(img)
    img.thumbnail(ICON_SIZE, Image.ANTIALIAS)

    # Strip all additional image info (mostly for ICC color
    # profiles, see issue #337)
    img.info.clear()
    return img


toremove = existing.difference(needed)
toupdate = existing.intersection(needed)
toadd = needed.difference(existing)


if toremove:
    print('Some icons are not used and will be removed:')
    for fname in sorted(toremove):
        fullname = '{}.png'.format(fname)
        print(('  {}'.format(fullname)))
        fullpath = os.path.join(icons_dir, fullname)
        os.remove(fullpath)

if toupdate:
    print(('Updating {} icons...'.format(len(toupdate))))
    missing = set()
    for fname in sorted(toupdate):
        icon = get_icon_file(fname)
        if icon is None:
            missing.add(fname)
            continue
        fullname = '{}.png'.format(fname)
        fullpath = os.path.join(icons_dir, fullname)
        icon.save(fullpath, 'png')
    if missing:
        print(('  {} icons are missing in export:'.format(len(missing))))
        for fname in sorted(missing):
            print(('    {}'.format(fname)))

if toadd:
    print(('Adding {} icons...'.format(len(toadd))))
    missing = set()
    for fname in sorted(toadd):
        icon = get_icon_file(fname)
        if icon is None:
            missing.add(fname)
            continue
        fullname = '{}.png'.format(fname)
        fullpath = os.path.join(icons_dir, fullname)
        icon.save(fullpath, 'png')
    if missing:
        print(('  {} icons are missing in export:'.format(len(missing))))
        for fname in sorted(missing):
            print(('    {}'.format(fname)))
