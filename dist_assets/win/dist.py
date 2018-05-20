# helper script to zip up pyinstaller distribution and create installer file

import os.path
from subprocess import call
import zipfile


def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

config = {}

exec(compile(open("config.py").read(), "config.py", 'exec'), config)

iscc =  "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" # inno script location via wine

print("Creating archive")

source = os.path.join(os.getcwd(), "dist", "pyfa")

fileName = "pyfa-{}-{}-{}-win".format(
    config['version'],
    config['expansionName'].lower(),
    config['expansionVersion']
)

archive = zipfile.ZipFile(os.path.join(os.getcwd(), "dist", fileName + ".zip"), 'w', compression=zipfile.ZIP_DEFLATED)
zipdir(source, archive)
archive.close()

print("Compiling EXE")

expansion = "%s %s" % (config['expansionName'], config['expansionVersion']),

call([
    iscc,
    os.path.join(os.getcwd(), "dist_assets", "win", "pyfa-setup.iss"),
    "/dMyAppVersion=%s" % (config['version']),
    "/dMyAppExpansion=%s" % (expansion),
    "/dMyAppDir=%s" % source,
    "/dMyOutputDir=%s" % os.path.join(os.getcwd(), "dist"),
    "/dMyOutputFile=%s" % fileName])  # stdout=devnull, stderr=devnull

print("Done")
