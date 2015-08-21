import config
import shutil
import time
import re
import os
import migrations

def getVersion(db):
    cursor = db.execute('PRAGMA user_version')
    return cursor.fetchone()[0]

def update(saveddata_engine):
    dbVersion = getVersion(saveddata_engine)
    appVersion = migrations.appVersion

    print dbVersion, appVersion

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

            func = migrations.updates[version+1]
            if func:
                print "applying update",version+1
                func(saveddata_engine)

        # when all is said and done, set version to current
        saveddata_engine.execute("PRAGMA user_version = {}".format(appVersion))
