import config
import shutil
import time
import re
import os

def getAppVersion():
    # calculate app version based on upgrade files we have
    appVersion = 0
    for fname in os.listdir(os.path.join(os.path.dirname(__file__), "migrations")):
        m = re.match("^upgrade(?P<index>\d+)\.py$", fname)
        if not m:
            continue
        index = int(m.group("index"))
        appVersion = max(appVersion, index)
    return appVersion

def getVersion(db):
    cursor = db.execute('PRAGMA user_version')
    return cursor.fetchone()[0]

def update(saveddata_engine):
    dbVersion = getVersion(saveddata_engine)
    appVersion = getAppVersion()

    if dbVersion == appVersion:
        return

    if dbVersion < appVersion:
        # Automatically backup database
        toFile = "%s/saveddata_migration_%d-%d_%s.db"%(
            config.savePath,
            dbVersion,
            appVersion,
            time.strftime("%Y%m%d_%H%M%S"))

        shutil.copyfile(config.saveDB, toFile)

        for version in xrange(dbVersion, appVersion):
            module = __import__("eos.db.migrations.upgrade{}".format(version + 1), fromlist=True)
            upgrade = getattr(module, "upgrade", False)
            if upgrade:
                upgrade(saveddata_engine)

        # when all is said and done, set version to current
        saveddata_engine.execute("PRAGMA user_version = {}".format(appVersion))
