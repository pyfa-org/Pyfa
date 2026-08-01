import requests
import os
import json
import wx
import sys

API_BASE = 'https://api.crowdin.com/api/v2'
PROJECT_IDENTIFIER = 'pyfa'
PAGE_LIMIT = 500

key = os.environ.get("CROWDIN_API_KEY", None)

if key is None or key == '':
    # if building from a forked PR, this is normal. Secret veariables are generally unavailable in those circumstances
    print("CROWDIN_API_KEY env variable not found, cannot fetch translation status.")
    sys.exit()

session = requests.Session()
session.headers.update({'Authorization': 'Bearer {}'.format(key)})


def errorMessage(resp):
    try:
        payload = resp.json()
    except ValueError:
        return '{} {}'.format(resp.status_code, resp.reason)

    error = payload.get('error')
    if isinstance(error, dict) and 'message' in error:
        return error['message']

    messages = []
    for entry in payload.get('errors', []):
        entry = entry.get('error', entry)
        for detail in entry.get('errors', []):
            if 'message' in detail:
                messages.append(detail['message'])
    if messages:
        return '; '.join(messages)

    return '{} {}'.format(resp.status_code, resp.reason)


def fetch(path, **params):
    params.setdefault('limit', PAGE_LIMIT)
    resp = session.get('{}/{}'.format(API_BASE, path), params=params)
    if resp.status_code != 200:
        print("failed to fetch crowdin progress: {}".format(errorMessage(resp)))
        sys.exit()
    return [x['data'] for x in resp.json()['data']]


projectId = os.environ.get("CROWDIN_PROJECT_ID", None)

if not projectId:
    projects = fetch('projects')
    projectId = next((x['id'] for x in projects if x.get('identifier') == PROJECT_IDENTIFIER), None)
    if projectId is None:
        print("Cannot find Crowdin project {!r}, is the API token scoped to it?".format(PROJECT_IDENTIFIER))
        sys.exit()

def availableLocales():
    localePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'locale')
    found = {}
    for name in sorted(os.listdir(localePath)):
        if not os.path.isdir(os.path.join(localePath, name)):
            continue
        info = wx.Locale.FindLanguageInfo(name)
        if info is not None:
            found[info.CanonicalName] = info
    return found


def matchLocale(code, locales):
    info = wx.Locale.FindLanguageInfo(code)
    if info is None:
        return None
    if info.CanonicalName in locales:
        return locales[info.CanonicalName]
    if '_' in info.CanonicalName:
        return None
    candidates = [x for name, x in locales.items() if name.split('_')[0] == info.CanonicalName]
    return candidates[0] if len(candidates) == 1 else None


locales = availableLocales()
data = []

for entry in fetch('projects/{}/languages/progress'.format(projectId)):
    code = entry['languageId'].replace('-', '_')
    lang = matchLocale(code, locales)
    if lang is None:
        print('Cannot find a match for ' + code)
        continue
    words = entry.get('words', {})
    phrases = entry.get('phrases', {})
    data.append({
        'code': code,
        'canonical_name': lang.CanonicalName,
        'name': lang.Description,
        'phrases': phrases.get('total'),
        'translated': phrases.get('translated'),
        'approved': phrases.get('approved'),
        'words': words.get('total'),
        'words_translated': words.get('translated'),
        'words_approved': words.get('approved'),
        'translated_progress': entry.get('translationProgress'),
        'approved_progress': entry.get('approvalProgress'),
    })

data = {x['canonical_name']: x for x in data}

with open("locale/progress.json", 'w') as file:
    file.seek(0)
    file.truncate()
    json.dump(data, file)
