import csv
import os
from shutil import copyfile

tqindex = '/home/av/.wine_eve/drive_c/EVE/SharedCache/tq/resfileindex.txt'

map = {}

with open(tqindex) as f:
    for row in csv.reader(f):
        if row[0].lower().startswith('res:/ui/texture/icons/'):
            map[row[0]] = row[1]

basepath = '/home/av/.wine_eve/drive_c/EVE/SharedCache/ResFiles'
outpath = '/home/av/Desktop/icons'

for resname, respath in map.items():
    newname = resname[len('res:/ui/texture/icons/'):].replace('/', '_')
    copyfile(os.path.join(basepath, respath), os.path.join(outpath, newname))
