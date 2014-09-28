import config

def getVersion(db):
    cursor = db.execute('PRAGMA user_version')
    return cursor.fetchone()[0]

def update(saveddata_engine):
    currversion = getVersion(saveddata_engine)

    if currversion == config.dbversion:
        return

    if currversion < config.dbversion:
        for version in xrange(currversion, config.dbversion):
            module = __import__('eos.db.migrations.upgrade%d'%(version+1), fromlist=True)
            upgrade = getattr(module, "upgrade", False)
            if upgrade:
                upgrade(saveddata_engine)

        # when all is said and done, set version to current
        saveddata_engine.execute('PRAGMA user_version = %d'%config.dbversion)
