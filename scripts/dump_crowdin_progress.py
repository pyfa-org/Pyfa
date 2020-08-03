import requests
import os
import json
import wx
import sys

key = os.environ.get("CROWDIN_API_KEY", None)

if key is None:
    # if building from a forked PR, this is normal. Secret veariables are generally unavailable in those circumstances
    print("CROWDIN_API_KEY env variable not found, cannot fetch translation status.")
    sys.exit()

print(key[0:2])

params = {
    'json': '',
    'key': key
}

resp = requests.get('https://api.crowdin.com/api/project/pyfa/status', params=params)
data = resp.json()

for x in data:
    x['code'] = x['code'].replace('-', '_')
    lang = wx.Locale.FindLanguageInfo(x['code'])
    if lang is None:
        print('Cannot find a match for '+x['code'])
        continue
    x['canonical_name'] = lang.CanonicalName

data = {x['canonical_name']: x for x in data}

with open("locale/progress.json", 'w') as file:
    file.seek(0)
    file.truncate()
    json.dump(data, file)