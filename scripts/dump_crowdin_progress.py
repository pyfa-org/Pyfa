import requests
import os
import json
import wx

key = os.environ.get("CROWDIN_API_KEY", "")

params = {
    'json': '',
    'key': key
}

resp = requests.get('https://api.crowdin.com/api/project/pyfa/status', params=params)
data = resp.json()
print(data)

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