#!/usr/bin/env python
"""
Script for generating distributables based on platform skeletons.

User supplies path for pyfa code base, root skeleton directory, and where the
builds go. The builds are automatically named depending on the pyfa config
values of `version` and `tag`. If it's a Stable release, the naming
convention is:

    pyfa-pyfaversion-expansion-expversion-platform

If it is not Stable (tag=git), we determine if the pyfa code base includes
the git repo to use as an ID. If not, uses randomly generated 6-character ID.
The unstable naming convention:

    pyfa-YYYMMDD-id-platform

dist.py can also build the Windows installer provided that it has a path to
Inno Setup (and, for generating on non-Windows platforms, that WINE is
installed). To build the EXE file, `win` must be included in the platforms to
be built.
"""

#@todo: ensure build directory can be written to
# todo: default build and dist directories

from optparse import OptionParser
import os.path
import shutil
import sys
import tarfile
import datetime
import random
import string
import zipfile
import errno
from subprocess import call

class FileStub():
    def write(self, *args):
        pass

    def flush(self, *args):
        pass

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst, ignore=loginfo)
    except: # python >2.5
        try:
            shutil.copy(src, dst)
        except:
            raise

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

skels = ['win', 'mac', 'src', 'win-wx3']
iscc =  "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" # inno script location via wine

if __name__ == "__main__":
    oldstd = sys.stdout
    parser = OptionParser()
    parser.add_option("-s", "--skeleton", dest="skeleton", help="Location of Pyfa-skel directory")
    parser.add_option("-b", "--base", dest="base", help="Location of cleaned read-only base directory")
    parser.add_option("-d", "--destination", dest="destination", help="Where to copy our distributable")
    parser.add_option("-p", "--platforms", dest="platforms", help="Comma-separated list of platforms to build", default="win,src,mac")
    parser.add_option("-q", "--quiet", dest="silent", action="store_true")
    parser.add_option("-w", "--winexe", dest="winexe", action="store_true", help="Build the Windows installer file (needs Inno Setup). Must include 'win' in platform options")
    parser.add_option("-z", "--zip", dest="zip", action="store_true", help="zip archive instead of tar")

    options, args = parser.parse_args()

    if options.skeleton is None or options.base is None or options.destination is None:
        print "Need --skeleton argument as well as --base and --destination argument"
        parser.print_help()
        sys.exit()

    if options.silent:
        sys.stdout = FileStub()

    options.platforms = options.platforms.split(",")

    #sys.path.append(options.base)
    #import config as pyfaconfig

    for skel in skels:
        if skel not in options.platforms:
            continue

        print "\n======== %s ========"%skel

        info = {}
        config = {}
        skeleton = os.path.expanduser(os.path.join(options.skeleton, skel))

        execfile(os.path.join(options.base, "config.py"), config)
        execfile(os.path.join(skeleton, "info.py"), info)

        destination = os.path.expanduser(options.destination)
        if not os.path.isdir(destination) or not os.access(destination, os.W_OK | os.X_OK):
            print "Destination directory does not exist or is not writable: {}".format(destination)
            sys.exit()

        dirName = info["arcname"]

        nowdt = datetime.datetime.now()
        now = "%04d%02d%02d" % (nowdt.year, nowdt.month, nowdt.day)

        git = False
        if config['tag'].lower() == "git":
            try: # if there is a git repo associated with base, use master commit
                with open(os.path.join(options.base, ".git", "refs", "heads", "master"), 'r') as f:
                    id = f.readline()[0:6]
                    git = True
            except: # else, use custom ID
                id = id_generator()
            fileName = "pyfa-{}-{}-{}".format(now, id, info["os"])
        else:
            fileName = "pyfa-{}-{}-{}-{}".format(
                config['version'],
                config['expansionName'].lower(),
                config['expansionVersion'],
                info["os"]
            )

        archiveName = "{}.{}".format(fileName, "zip" if options.zip else "tar.bz2")
        dst = os.path.join(os.getcwd(), dirName) # tmp directory where files are copied
        tmpFile = os.path.join(os.getcwd(), archiveName)

        i = 0
        ignoreData = (".git", ".gitignore", ".gitmodules", "dist_assets", "build", "dist", "scripts", ".idea")
        def loginfo(path, names):
            # Print out a "progress" and return directories / files to ignore
            global i
            i += 1
            if i % 10 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            return ignoreData

        try:
            print "Copying skeleton to ", dst
            i = 0
            shutil.copytree(skeleton, dst, ignore=loginfo)
            print
            if "win-wx3" not in skel:
                # simply copying base into working build
                base = os.path.join(dst, info["base"])
                print "Copying base to ", base

                i = 0
                for stuff in os.listdir(os.path.expanduser(options.base)):
                    currSource = os.path.join(os.path.expanduser(options.base), stuff)
                    currDest = os.path.join(base, stuff)
                    if stuff in ignoreData:
                        continue
                    elif os.path.isdir(currSource):
                        shutil.copytree(currSource, currDest, ignore=loginfo)
                    else:
                        shutil.copy2(currSource, currDest)

                print
                print "Copying done, making archive: ", tmpFile
            else:
                # this should work, but it's barely been tested
                base = os.path.join(dst, info["base"])
                source = os.path.expanduser(options.base)
                sys.path.append(source)
                import setup

                # the following operations require us to be in the source directory
                # for the zipping to work correctly
                oldcwd = os.getcwd()
                os.chdir(source)

                libraryFile = os.path.join(base, "library.zip")

                with zipfile.ZipFile(libraryFile, 'a') as library:
                    for dir in setup.packages:
                        zipdir(dir, library)
                    library.write('pyfa.py', 'pyfa__main__.py')
                    library.write('config.py')

                for dir in setup.include_files:
                    copyanything(dir, os.path.join(base, dir))

                # @todo: this is in win-wx3 for now, but it will have to be migrated to  OS X release when wx3 is merged into master. This must be tested
                imagesFile = os.path.join(base, "imgs.zip")

                with zipfile.ZipFile(imagesFile, 'w') as images:
                    os.chdir('imgs')  # need to be in images directory
                    for dir in setup.icon_dirs:
                        zipdir(dir, images)

                os.chdir(oldcwd)

            if options.zip:
                archive = zipfile.ZipFile(tmpFile, 'w', compression=zipfile.ZIP_DEFLATED)
                zipdir(dirName, archive)
                archive.close()
            else:
                archive = tarfile.open(tmpFile, "w:bz2")
                archive.add(dst, arcname=info["arcname"])
                archive.close()

            print "Moving archive to ", destination
            shutil.move(tmpFile, destination)

            if "win" in skel and options.winexe:
                print "Compiling EXE"

                if config['tag'].lower() == "git":
                    if git:   # if git repo info available, use git commit
                        expansion = "git-%s"%(id)
                    else: # if there is no git repo, use timestamp
                        expansion = now
                else: # if code is Stable, use expansion name
                   expansion = "%s %s"%(config['expansionName'], config['expansionVersion']),

                calllist = ["wine"] if 'win' not in sys.platform else []

                call(calllist + [
                    iscc,
                    os.path.join(os.path.dirname(__file__), "pyfa-setup.iss"),
                    "/dMyAppVersion=%s"%(config['version']),
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
