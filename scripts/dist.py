#!/usr/bin/env python

'''
Script for generating distributables based on platform skeletons.
'''

from optparse import OptionParser
import os.path
import shutil
import tempfile
import sys
import tarfile
import datetime
import random
import string
import zipfile
from subprocess import call

class FileStub():
    def write(self, *args):
        pass

    def flush(self, *args):
        pass

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

skels = ['win', 'mac', 'src']
iscc =  "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" # inno script location via wine

if __name__ == "__main__":
    oldstd = sys.stdout
    parser = OptionParser()
    parser.add_option("-s", "--skeleton", dest="skeleton", help="Location of Pyfa-skel directory")
    parser.add_option("-b", "--base", dest="base", help="Location of cleaned read-only base directory")
    parser.add_option("-d", "--destination", dest="destination", help="Where to copy our distributable")
    parser.add_option("-p", "--platforms", dest="platforms", help="Comma-separated list of platforms to build", default="win,src,mac")
    parser.add_option("-t", "--static", dest="static", help="Directory containing static files")
    parser.add_option("-q", "--quiet", dest="silent", action="store_true")
    parser.add_option("-w", "--winexe", dest="winexe", action="store_true", help="Build the Windows installer file (needs Inno Setup)")
    parser.add_option("-z", "--zip", dest="zip", action="store_true", help="zip archive instead of tar")

    options, args = parser.parse_args()

    if options.skeleton is None or options.base is None or options.destination is None:
        print "Need --skeleton argument as well as --base and --destination argument"
        parser.print_help()
        sys.exit()

    if options.silent:
        sys.stdout = FileStub()

    options.platforms = options.platforms.split(",")

    sys.path.append(options.base)
    import config as pyfaconfig

    for skel in skels:
        if skel not in options.platforms:
            continue

        print "\n======== %s ========"%skel
        infoDict = {}
        skeleton = os.path.expanduser(os.path.join(options.skeleton, skel))
        info = execfile(os.path.join(skeleton, "info.py"), infoDict)
        dirName = infoDict["arcname"]
        nowdt = datetime.datetime.now()
        now = "%04d%02d%02d" % (nowdt.year, nowdt.month, nowdt.day)
        git = False
        if pyfaconfig.tag.lower() == "git":
            try: # if there is a git repo associated with base, use master commit
                with open(os.path.join(options.base,"..",".git","refs","heads","master"), 'r') as f:
                    id = f.readline()[0:6]
                    git = True
            except: # else, use custom ID
                id = id_generator()
            fileName = "pyfa-%s-%s-%s" % (now, id, infoDict["os"])
        else:
            fileName = "pyfa-%s-%s-%s-%s" % (pyfaconfig.version, pyfaconfig.expansionName.lower(), pyfaconfig.expansionVersion, infoDict["os"])

        archiveName = "%s.%s"%(fileName, "zip" if options.zip else "tar.bz2")
        dst = os.path.join(os.getcwd(), dirName) # tmp directory where files are copied
        tmpFile = os.path.join(os.getcwd(), archiveName)
        config = os.path.join(skeleton, "config.py")
        destination = os.path.expanduser(options.destination)

        i = 0
        gitData = (".git", ".gitignore", ".gitmodules")
        def loginfo(path, names):
            global i
            i += 1
            if i % 10 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            return gitData

        try:
            print "Copying skeleton to ", dst
            i = 0
            shutil.copytree(skeleton, dst, ignore=loginfo)
            print
            base = os.path.join(dst, infoDict["base"])
            print "Copying base to ", base

            i = 0
            for stuff in os.listdir(os.path.expanduser(options.base)):
                currSource = os.path.join(os.path.expanduser(options.base), stuff)
                currDest = os.path.join(base, stuff)
                if stuff in gitData:
                    continue
                elif os.path.isdir(currSource):
                    shutil.copytree(currSource, currDest, ignore=loginfo)
                else:
                    shutil.copy2(currSource, currDest)

            print

            if os.path.exists(config):
                print "Adding skeleton config file"
                shutil.copy2(config, base)


            if options.static is not None and os.path.exists(os.path.expanduser(options.static)):
                print "Copying static data to ", os.path.join(base, "staticdata")
                static = os.path.expanduser(options.static)
                shutil.copytree(static, os.path.join(base, "staticdata"), ignore=loginfo)

            print "Copying done, making archive: ", tmpFile

            if options.zip:
                archive = zipfile.ZipFile(tmpFile, 'w', compression=zipfile.ZIP_DEFLATED)
                zipdir(dirName, archive)
                archive.close()
            else:
                archive = tarfile.open(tmpFile, "w:bz2")
                archive.add(dst, arcname=infoDict["arcname"])
                archive.close()

            print "Moving archive to ", destination
            shutil.move(tmpFile, destination)

            if "win" in skel and options.winexe:
                print "Compiling EXE"

                if pyfaconfig.tag.lower() == "git":
                    if git:   # if git repo info available, use git commit
                        expansion = "git-%s"%(id)
                    else: # if there is no git repo, use timestamp
                        expansion = now
                else: # if code is Stable, use expansion name
                   expansion = "%s %s"%(pyfaconfig.expansionName, pyfaconfig.expansionVersion),

                calllist = ["wine"] if 'win' not in sys.platform else []

                call(calllist + [
                    iscc,
                    os.path.join(os.path.dirname(__file__), "pyfa-setup.iss"),
                    "/dMyAppVersion=%s"%(pyfaconfig.version),
                    "/dMyAppExpansion=%s"%(expansion),
                    "/dMyAppDir=%s"%dst,
                    "/dMyOutputDir=%s"%destination,
                    "/dMyOutputFile=%s"%fileName]) #stdout=devnull, stderr=devnull

                print "EXE completed"
                
        except Exception as e:
            print "Encountered an error: \n\t", e
            raise
        finally:
            print "Deleting tmp files\n"
            try:
                try:
                    shutil.rmtree("dist") # Inno dir
                except:
                    pass
                shutil.rmtree(dst)
                os.unlink(tmpFile)
            except:
                pass

        sys.stdout = oldstd
        if os.path.isdir(destination):
            print os.path.join(destination, os.path.split(tmpFile)[1])
        else:
            print destination
