from logbook import Logger
import shutil
import time

import config
from . import migrations

pyfalog = Logger(__name__)


class _MigrationResult:
    def __init__(self, rows):
        self._rows = rows

    def __iter__(self):
        return iter(self._rows)

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def scalar(self):
        return self._rows[0][0] if self._rows else None


class _MigrationConnection:
    """
    SQLAlchemy 1 compatibility, where it was possible to use connectionless queries
    """

    def __init__(self, connection):
        self._connection = connection

    def execute(self, statement, parameters=None):
        if parameters is None:
            result = self._connection.exec_driver_sql(statement)
        else:
            result = self._connection.exec_driver_sql(statement, parameters)
        rows = result.fetchall() if result.returns_rows else None
        self._connection.commit()
        return _MigrationResult(rows) if rows is not None else result


def getVersion(saveddata_engine):
    with saveddata_engine.connect() as connection:
        return connection.exec_driver_sql('PRAGMA user_version').scalar()


def getAppVersion():
    return migrations.appVersion


def update(saveddata_engine):
    dbVersion = getVersion(saveddata_engine)
    appVersion = getAppVersion()

    if dbVersion == appVersion:
        return

    if dbVersion < appVersion:
        # Automatically backup database
        toFile = "%s/saveddata_migration_%d-%d_%s.db" % (
            config.savePath,
            dbVersion,
            appVersion,
            time.strftime("%Y%m%d_%H%M%S"))

        shutil.copyfile(config.saveDB, toFile)

        with saveddata_engine.connect() as connection:
            wrapped = _MigrationConnection(connection)

            for version in range(dbVersion, appVersion):
                func = migrations.updates[version + 1]
                if func:
                    pyfalog.info("Applying database update: {0}", version + 1)
                    func(wrapped)

            # when all is said and done, set version to current
            wrapped.execute("PRAGMA user_version = {}".format(appVersion))
