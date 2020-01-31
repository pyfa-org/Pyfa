# helper script to zip up pyinstaller distribution and create installer file

import os.path
from subprocess import call
import zipfile
from packaging.version import Version
import yaml


with open("version.yml", 'r') as file:
    data = yaml.load(file, Loader=yaml.SafeLoader)
    version = data['version']

os.environ["PYFA_DIST_DIR"] = os.path.join(os.getcwd(), 'dist')

os.environ["PYFA_VERSION"] = version
iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

source = os.path.join(os.environ["PYFA_DIST_DIR"], "pyfa")

fileName = "pyfa-{}-win".format(os.environ["PYFA_VERSION"])

print("Compiling EXE")

v = Version(version)

print(v)

call([
    iscc,
    os.path.join(os.getcwd(), "dist_assets", "win", "pyfa-setup.iss"),
    "/dMyAppVersion=%s" % v,
    "/dMyAppDir=%s" % source,
    "/dMyOutputDir=%s" % os.path.join(os.getcwd()),
    "/dMyOutputFile=%s" % fileName])  # stdout=devnull, stderr=devnull

print("Done")
