'''
A change to EVE Online's cache format rendered Reverence unable to correctly dump the icons file. As a stop gap, this
reads the offical SDE iconIDs.yaml and populates our own icons.json file. This files should then be transferred to the
other JSON files Phobos dumps before being converted to SQL
'''

import yaml
import json

iconDict = {}

stream = open('iconIDs.yaml', 'r')
docs = yaml.load_all(stream)

for doc in docs:
    for k,v in list(doc.items()):
        iconDict[str(k)] = {'iconFile': v['iconFile']}

with open('icons.json', 'w') as outfile:
    json.dump(iconDict, outfile)

print('done')
