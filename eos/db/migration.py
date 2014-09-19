import sqlalchemy

def update(saveddata_engine):
    checkPriceFailures(saveddata_engine)
    checkApiDefaultChar(saveddata_engine)
    checkFitBooster(saveddata_engine)
    checktargetResists(saveddata_engine)

def checkPriceFailures(saveddata_engine):
    # Check if we have 'failed' column
    try:
        saveddata_engine.execute("SELECT failed FROM prices")
    except sqlalchemy.exc.DatabaseError:
        # As we don't have any important data there, let's just drop
        # and recreate whole table
        from eos.db.saveddata.price import prices_table
        # Attempt to drop/create table only if it's already there
        try:
            prices_table.drop(saveddata_engine)
            prices_table.create(saveddata_engine)
        except sqlalchemy.exc.DatabaseError:
            pass


def checkApiDefaultChar(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT * FROM characters LIMIT 1")
    # If table doesn't exist, it means we're doing everything from scratch
    # and sqlalchemy will process everything as needed
    except sqlalchemy.exc.DatabaseError:
        pass
    # If not, we're running on top of existing DB
    else:
        # Check that we have columns
        try:
            saveddata_engine.execute("SELECT defaultChar, chars FROM characters LIMIT 1")
        # If we don't, create them
        # This is ugly as hell, but we can't use proper migrate packages as it
        # will require us to rebuild skeletons, including mac
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE characters ADD COLUMN defaultChar INTEGER;")
            saveddata_engine.execute("ALTER TABLE characters ADD COLUMN chars VARCHAR;")

def checkFitBooster(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT * FROM fits LIMIT 1")
    # If table doesn't exist, it means we're doing everything from scratch
    # and sqlalchemy will process everything as needed
    except sqlalchemy.exc.DatabaseError:
        pass
    # If not, we're running on top of existing DB
    else:
        # Check that we have columns
        try:
            saveddata_engine.execute("SELECT booster FROM fits LIMIT 1")
        # If we don't, create them
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE fits ADD COLUMN booster BOOLEAN;")
        # Set NULL data to 0 (needed in case of downgrade, see GH issue #62
        saveddata_engine.execute("UPDATE fits SET booster = 0 WHERE booster IS NULL;")

def checktargetResists(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT * FROM fits LIMIT 1")
    # If table doesn't exist, it means we're doing everything from scratch
    # and sqlalchemy will process everything as needed
    except sqlalchemy.exc.DatabaseError:
        pass
    # If not, we're running on top of existing DB
    else:
        # Check that we have columns
        try:
            saveddata_engine.execute("SELECT targetResistsID FROM fits LIMIT 1")
        # If we don't, create them
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE fits ADD COLUMN targetResistsID INTEGER;")
