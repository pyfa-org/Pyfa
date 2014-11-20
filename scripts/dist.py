#!/usr/bin/env python

from optparse import OptionParser
import os.path
import shutil
import tempfile
import sys
import tarfile
import datetime
import random
import string

class FileStub():
    def write(self, *args):
        pass

    def flush(self, *args):
        pass

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

if __name__ == "__main__":
    oldstd = sys.stdout
    parser = OptionParser()
    parser.add_option("-s", "--skeleton", dest="skeleton", help="Location of skeleton directory")
    parser.add_option("-b", "--base", dest="base", help="location of the base directory")
    parser.add_option("-d", "--destination", dest="destination", help="where to copy our archive")
    parser.add_option("-t", "--static", dest="static", help="directory containing static files")
    parser.add_option("-q", "--quiet", dest="silent", action="store_true")
    options, args = parser.parse_args()

    if options.skeleton is None or options.base is None or options.destination is None:
        print "Need --skeleton argument as well as --base and --destination argument"
        parser.print_help()
        sys.exit()

    if options.silent:
        sys.stdout = FileStub()

    randomId = id_generator()
    infoDict = {}
    skeleton = os.path.expanduser(options.skeleton)
    info = execfile(os.path.join(skeleton, "info.py"), infoDict)
    now = datetime.datetime.now()
    now = "%04d%02d%02d" % (now.year, now.month, now.day)
    dirName = "nighty-build-%s-%s" % (now, randomId)
    dst = os.path.join(os.getcwd(), dirName)
    tmpFile = os.path.join(os.getcwd(), "nighty-build-%s-%s-%s.tar.bz2" % (now, infoDict["os"], randomId))
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
        print "copying skeleton to ", dst
        i = 0
        shutil.copytree(skeleton, dst, ignore=loginfo)
        print ""

        base = os.path.join(dst, infoDict["base"])
        print "copying base to ", base

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

        print ""
        if os.path.exists(config):
            print "adding skeleton config file"
            shutil.copy2(config, base)


        if options.static is not None and os.path.exists(os.path.expanduser(options.static)):
            print "copying static data to ", os.path.join(base, "staticdata")
            static = os.path.expanduser(options.static)
            shutil.copytree(static, os.path.join(base, "staticdata"), ignore=loginfo)

        print "removing development data"
        paths = []
        paths.append(os.path.join(base, "eos", "tests"))
        paths.append(os.path.join(base, "eos", "utils", "scripts"))
        for path in paths:
            if os.path.exists(path):
                print path
                shutil.rmtree(path)


        print "copying done, making archive: ", tmpFile
        archive = tarfile.open(tmpFile, "w:bz2")
        print "making archive"
        archive.add(dst, arcname=infoDict["arcname"])
        print "closing"
        archive.close()
        print "copying archive to ", destination
        shutil.move(tmpFile, destination)
    except:
        print "encountered an error"
        raise
    finally:
        print "deleting tmp files"
        try:
            shutil.rmtree(dst)
            os.unlink(tmpFile)
        except:
            pass

    sys.stdout = oldstd
    if os.path.isdir(destination):
        print os.path.join(destination, os.path.split(tmpFile)[1])
    else:
        print destination
