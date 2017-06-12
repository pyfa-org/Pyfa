#!/usr/bin/env python3

"""
This script updates ship renders and removes unused ones.
"""


import argparse
import os
import re
import sqlite3

from PIL import Image


parser = argparse.ArgumentParser(description='This script updates ship renders for pyfa')
parser.add_argument('-r', '--renders', required=True, type=str, help='path to unpacked Renders folder from CCP\'s image export')
args = parser.parse_args()


script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(script_dir, '..', 'eve.db'))
icons_dir = os.path.abspath(os.path.join(script_dir, '..', 'imgs', 'renders'))
export_dir = os.path.abspath(os.path.expanduser(args.renders))


db = sqlite3.connect(db_path)
cursor = db.cursor()

RENDER_SIZE = (32, 32)


query_ships = 'select it.typeID from invtypes as it inner join invgroups as ig on it.groupID = ig.groupID where ig.categoryID in (6, 65)'


needed = set()
existing = set()
export = set()


for row in cursor.execute(query_ships):
    needed.add(row[0])

for container, filedir in (
    (existing, icons_dir),
    (export, export_dir)
):
    for fname in os.listdir(filedir):
        if not os.path.isfile(os.path.join(filedir, fname)):
            continue
        m = re.match(r'^(?P<typeid>\d+)\.png', fname)
        if not m:
            continue
        container.add(int(m.group('typeid')))

toremove = existing.difference(needed)
toupdate = existing.intersection(needed)
toadd = needed.difference(existing)


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


def get_render(type_id):
    fname = '{}.png'.format(type_id)
    fullpath = os.path.join(export_dir, fname)
    img = Image.open(fullpath)
    if img.size != RENDER_SIZE:
        img = crop_image(img)
        img.thumbnail(RENDER_SIZE, Image.ANTIALIAS)
    # Strip all additional image info (mostly for ICC color
    # profiles, see issue #337)
    img.info.clear()
    return img


if toremove:
    print('Some renders are not used and will be removed:')
    for type_id in sorted(toremove):
        fullname = '{}.png'.format(type_id)
        print(('  {}'.format(fullname)))
        fullpath = os.path.join(icons_dir, fullname)
        os.remove(fullpath)

if toupdate:
    print(('Updating {} renders...'.format(len(toupdate))))
    missing = toupdate.difference(export)
    toupdate.intersection_update(export)
    for type_id in sorted(toupdate):
        render = get_render(type_id)
        fname = '{}.png'.format(type_id)
        fullpath = os.path.join(icons_dir, fname)
        render.save(fullpath, 'png')
    if missing:
        print(('  {} renders are missing in export:'.format(len(missing))))
        for type_id in sorted(missing):
            print(('    {}.png'.format(type_id)))

if toadd:
    print(('Adding {} renders...'.format(len(toadd))))
    missing = toadd.difference(export)
    toadd.intersection_update(export)
    for type_id in sorted(toadd):
        render = get_render(type_id)
        fname = '{}.png'.format(type_id)
        fullpath = os.path.join(icons_dir, fname)
        render.save(fullpath, 'png')
    if missing:
        print(('  {} renders are missing in export:'.format(len(missing))))
        for type_id in sorted(missing):
            print(('    {}.png'.format(type_id)))
