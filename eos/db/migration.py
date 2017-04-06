from logbook import Logger
import shutil
import time

import config
from eos.db.migrations import (
    upgrade1,
    upgrade2,
    upgrade3,
    upgrade4,
    upgrade5,
    upgrade6,
    upgrade7,
    upgrade8,
    upgrade9,
    upgrade10,
    upgrade11,
    upgrade12,
    upgrade13,
    upgrade14,
    upgrade15,
    upgrade16,
    upgrade17,
    upgrade18,
    upgrade19,
    upgrade20,
    upgrade21,
    upgrade22,
)

pyfalog = Logger(__name__)


def getVersion(db):
    cursor = db.execute('PRAGMA user_version')
    return cursor.fetchone()[0]


def update(saveddata_engine):
    pyfalog.info("Database upgrade in progress.")
    dbVersion = True

    while dbVersion is True:
        dbVersion = getVersion(saveddata_engine)

        current_upgrade = "upgrade" + str(dbVersion + 1)
        try:
            upgrade_class = globals()[current_upgrade]
            pyfalog.info("Upgrading database from version {0} to {1}", dbVersion, current_upgrade)
        except:
            upgrade_class = None
            pyfalog.info("No updates found from version {0} to {1}", dbVersion, current_upgrade)
            break

        # Automatically backup database
        toFile = "%s/saveddata_migration_%d-%d_%s.db" % (
            config.savePath,
            dbVersion,
            dbVersion + 1,
            time.strftime("%Y%m%d_%H%M%S"))
        shutil.copyfile(config.saveDB, toFile)

        if upgrade_class:
            try:
                pyfalog.info("Running upgrade.")
                getattr(upgrade_class, 'upgrade')(saveddata_engine)
            except Exception as e:
                exit_message = "Upgrade failed. Please revert to the last database version and report this error to the developers."
                pyfalog.critical(exit_message)
                e.message = e.message + "\n\n" + exit_message
                raise

        # when all is said and done, set version to current
        saveddata_engine.execute("PRAGMA user_version = {}".format(dbVersion + 1))

    pyfalog.info("Database upgrade complete.")