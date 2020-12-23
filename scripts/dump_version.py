"""
This script is solely used when generating builds. It generates a version number automatically using
git tags as it's basis. Whenever a build is created, run this file beforehand and it should replace
the old version number with the new one in VERSION.YML
"""

import yaml
import subprocess
import os

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


with open("version.yml", 'r+') as file:
    data = yaml.load(file, Loader=yaml.SafeLoader)
    file.seek(0)
    file.truncate()
    # todo: run Version() on the tag to ensure that it's of proper formatting - fail a test if not and prevent building
    # python's versioning spec doesn't handle the same format git describe outputs, so convert it.
    label = os.environ["PYFA_VERSION"].split('-') if "PYFA_VERSION" in os.environ else subprocess.check_output(["git", "describe", "--tags"]).strip().decode().split('-')
    label = '-'.join(label[:-2])+'+'+'-'.join(label[-2:]) if len(label) > 1 else label[0]
    label = rreplace(label, '+', '-', label.count('+') - 1)
    print(label)
    data['version'] = label
    yaml.dump(data, file, default_flow_style=False)

