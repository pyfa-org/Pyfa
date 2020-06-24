def convert_modules(engine, conversions):
    '''Converts modules based on tiericide conversion mappings.

    :param engine:
    :param conversions:
    :return:
    '''
    for replacement_item, list in conversions.items():
        for retired_item in list:
            engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                           (replacement_item, retired_item))
            engine.execute('UPDATE "modules" SET "baseItemID" = ? WHERE "baseItemID" = ?',
                           (replacement_item, retired_item))
            engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                           (replacement_item, retired_item))