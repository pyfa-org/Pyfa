import config
import shutil
import time
import os

def getVersion(db):
    cursor = db.execute('PRAGMA user_version')
    return cursor.fetchone()[0]

def update(saveddata_engine):
    dbVersion = getVersion(saveddata_engine)

    files = os.listdir(os.path.join(os.path.dirname(__file__), "migrations"))
    appVersion = len([f for f in files if f.startswith("upgrade")])

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
            module = __import__('eos.db.migrations.upgrade%d'%(version+1), fromlist=True)
            upgrade = getattr(module, "upgrade", False)
            if upgrade:
                upgrade(saveddata_engine)

        # when all is said and done, set version to current
        saveddata_engine.execute('PRAGMA user_version = %d'%appVersion)
