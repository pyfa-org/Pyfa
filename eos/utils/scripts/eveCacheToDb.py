#!/usr/bin/env python
#===============================================================================
# Copyright (C) 2010 Anton Vorobyov
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

'''
This script pulls data out of EVE cache and makes a database dump. To get most of the data,
you need to just log into game; however, for some special data sometimes you need to dump
it by executing corresponding action in game, for example - open market tree to get data for
invmarketgroups table.
Reverence library by Entity is used, check http://wiki.github.com/ntt/reverence/ for info
As reverence uses the same Python version as EVE client (2.x series), script cannot be converted to python3
Example commands to run the script under Linux with default eve paths for getting SQLite dump:
Tranquility: python eveCacheToDb.py --eve="~/.wine/drive_c/Program Files/CCP/EVE" --cache="~/.wine/drive_c/users/"$USER"/Local Settings/Application Data/CCP/EVE/c_program_files_ccp_eve_tranquility/cache" --dump="sqlite:////home/"$USER"/Desktop/eve.db"
Singularity: python eveCacheToDb.py --eve="~/.wine/drive_c/Program Files/CCP/Singularity" --cache="~/.wine/drive_c/users/"$USER"/Local Settings/Application Data/CCP/EVE/c_program_files_ccp_singularity_singularity/cache" --sisi --dump="sqlite:////home/"$USER"/Desktop/evetest.db"
'''

import os
import sys

# Add eos root path to sys.path
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..", "..", "..")))

def get_map():
    """
    Return table name - table class map
    """
    return {"allianceshortnames": None,
            "billtypes": None,
            "certificaterelationships": None,
            "certificates": None,
            "corptickernames": None,
            "dgmattribs": AttributeInfo,
            "dgmeffects": EffectInfo,
            "dgmtypeattribs": Attribute,
            "dgmtypeeffects": Effect,
            "evegraphics": None,
            "evelocations": None,
            "eveowners": None,
            "eveunits": Unit,
            "groupsByCategories": None,
            "icons": Icon,
            "invbptypes": None,
            "invcategories": Category,
            "invcontrabandTypesByFaction": None,
            "invcontrabandTypesByType": None,
            "invgroups": Group,
            "invmetagroups": MetaGroup,
            "invmarketgroups": MarketGroup,
            "invmetatypes": MetaType,
            "invmetatypesByTypeID": None,
            "invreactiontypes": None,
            "invtypes": Item,
            "locationscenes": None,
            "locationwormholeclasses": None,
            "mapcelestialdescriptions": None,
            "ownericons": None,
            "ramactivities": None,
            "ramaltypes": None,
            "ramaltypesdetailpercategory": None,
            "ramaltypesdetailpergroup": None,
            "ramcompletedstatuses": None,
            "ramtyperequirements": None,
            "schematics": None,
            "schematicsByPin": None,
            "schematicsByType": None,
            "schematicspinmap": None,
            "schematicstypemap": None,
            "shiptypes": None,
            "sounds": None,
            "typesByGroups": None,
            "typesByMarketGroups": None}

def get_order():
    """
    Return order for table processing
    """
    return ("icons",
            "invmarketgroups",
            "eveunits",
            "dgmattribs",
            "dgmeffects",
            "invcategories",
            "invgroups",
            "invmetagroups",
            "invtypes",
            "invmetatypes",
            "dgmtypeattribs",
            "dgmtypeeffects")

def get_customcalls():
    """
    Return custom table - call to get data for it map
    """
    return {"invmarketgroups": eve.RemoteSvc("marketProxy").GetMarketGroups()}

def process_table(sourcetable, tablename, tableclass):
    """
    Get all data from cache and write it to database
    """
    # Get data from source and process it
    tabledata = get_table_data(sourcetable, tablename, get_source_headers(sourcetable))
    # Insert everything into table
    insert_table_values(tabledata, tableclass)
    return

def get_source_headers(sourcetable):
    """
    Pull list of headers from the source table
    """
    sourceheaders = None
    guid = getattr(sourcetable, "__guid__", "None")
    # For IndexRowset and IndexedRowLists Reverence provides list of headers
    if guid in ("util.IndexRowset", "util.FilterRowset"):
        sourceheaders = tuple(sourcetable.header)
    # For IndexedRowLists, we need to compose list ourselves
    elif guid == "util.IndexedRowLists":
        headerset = set()
        for item in sourcetable:
            for row in sourcetable[item]:
                for headername in row.__header__.Keys():
                    headerset.add(headername)
        sourceheaders = tuple(headerset)
    return sourceheaders

def get_table_data(sourcetable, tablename, headers):
    """
    Pull data out of source table
    """
    # Each row is enclosed into dictionary, full table is list of these dictionaries
    datarows = []
    guid = getattr(sourcetable, "__guid__", "None")
    # We have Select method for IndexRowset tables
    if guid == "util.IndexRowset":
        for values in sourcetable.Select(*headers):
            # When Select is asked to find single value, it is returned in its raw
            # form. Convert is to tuple for proper further processing
            if not isinstance(values, (list, tuple, set)):
                values = (values,)
            headerslen = len(headers)
            datarow = {}
            # 1 row value should correspond to 1 header, if number or values doesn't
            # correspond to number of headers then something went wrong
            if headerslen != len(values):
                print "Error: malformed data in source table {0}".format(tablename)
                return None
            # Fill row dictionary with values and append it to list
            for i in xrange(headerslen):
                # If we've got ASCII string, convert it to Unicode
                if isinstance(values[i], str):
                    datarow[headers[i]] = unicode(values[i], 'ISO-8859-1')
                else:
                    datarow[headers[i]] = values[i]
            datarows.append(datarow)
    # FilterRowset and IndexedRowLists are accessible almost like dictionaries
    elif guid in ("util.FilterRowset", "util.IndexedRowLists"):
        # Go through all source table elements
        for element in sourcetable.iterkeys():
            # Go through all rows of an element
            for row in sourcetable[element]:
                datarow = {}
                # Fill row dictionary with values we need and append it to the list
                for header in headers:
                    value = getattr(row, header, None)
                    # None and zero values are different, and we want to write zero
                    # values to database
                    if value or value in (0, 0.0):
                        datarow[header] = value
                datarows.append(datarow)

    return datarows

def insert_table_values(tabledata, tableclass):
    """
    Insert values into tables and show progress
    """
    rows = 0
    rows_skipped = 0
    # Go through all table rows
    for row in tabledata:
        instance = tableclass()
        # Print dot each 1k inserted rows
        if rows / 1000.0 == int(rows / 1000.0):
            sys.stdout.write(".")
            sys.stdout.flush()
        try:
            # Go through all fields of a row, process them and insert
            for header in row:
                setattr(instance, header, process_value(row[header], tableclass, header))
            eos.db.gamedata_session.add(instance)
            rows += 1
        except ValueError:
            rows_skipped += 1
    # Print out results and actually commit results to database
    print "\nInserted {0} rows. skipped {1} rows".format(rows, rows_skipped)
    eos.db.gamedata_session.commit()

def process_value(value, tableclass, header):
    # Get column info
    info = tableclass._sa_class_manager.mapper.c.get(header)
    if info is None:
        return

    # Null out non-existent foreign key relations
    foreign_keys = info.foreign_keys
    if len(foreign_keys) > 0:
        for key in foreign_keys:
            col = key.column
            if not query_existence(col, value) and not key.deferrable:
                if info.nullable:
                    return None
                else:
                    raise ValueError("Integrity check failed")
            else:
                return value
    #Turn booleans into actual booleans, don't leave them as integers
    elif type(info.type) == Boolean:
        return bool(value)
    else:
        return value

existence_cache = {}
def query_existence(col, value):
    key = (col, col.table, value)
    info = existence_cache.get(key)
    if info is None:
        info = eos.db.gamedata_session.query(col.table).filter(col == value).count() > 0
        existence_cache[key] = info

    return info

if __name__ == "__main__":
    from ConfigParser import ConfigParser
    from optparse import OptionParser

    from reverence import blue
    from sqlalchemy import Boolean
    from sqlalchemy.orm import class_mapper, ColumnProperty

    import eos.config

    # Parse command line options
    usage = "usage: %prog --eve=EVE --cache=CACHE --dump=DUMP [--release=RELEASE --sisi]"
    parser = OptionParser(usage=usage)
    parser.add_option("-e", "--eve", help="path to eve folder")
    parser.add_option("-c", "--cache", help="path to eve cache folder")
    parser.add_option("-d", "--dump", help="the SQL Alchemy connection string of where we should place our final dump")
    parser.add_option("-r", "--release", help="database release number, defaults to 1", default="1")
    parser.add_option("-s", "--sisi", action="store_true", dest="singularity", help="if you're going to work with Singularity test server data, use this option", default=False)
    (options, args) = parser.parse_args()


    # Exit if we do not have any of required options
    if not options.eve or not options.cache or not options.dump:
        sys.stderr.write("You need to specify paths to eve folder, cache folder and SQL Alchemy connection string. Run script with --help option for further info.\n")
        sys.exit()

    # We can deal either with singularity or tranquility servers
    if options.singularity: server = "singularity"
    else: server = "tranquility"

    # Set static variables for paths
    PATH_EVE = os.path.expanduser(options.eve)
    PATH_CACHE = os.path.expanduser(options.cache)

    eos.config.gamedata_connectionstring = options.dump
    eos.config.debug = False

    from eos.gamedata import *
    import eos.db

    # Get version of EVE client
    config = ConfigParser()
    config.read(os.path.join(PATH_EVE, "common.ini"))

    # Form metadata dictionary for corresponding table
    metadata = {}
    metadata["version"] = config.getint("main", "build")
    metadata["release"] = options.release

    # Initialize Reverence cache manager
    eve = blue.EVE(PATH_EVE, cachepath=PATH_CACHE, server=server)
    cfg = eve.getconfigmgr()

    # Create all tables we need
    eos.db.gamedata_meta.create_all()

    # Add versioning info to the metadata table
    for fieldname in metadata:
        eos.db.gamedata_session.add(MetaData(fieldname, metadata[fieldname]))

    eos.db.gamedata_session.commit()

    # Get table map, processing order and special table data
    TABLE_MAP = get_map()
    TABLE_ORDER = get_order()
    CUSTOM_CALLS = get_customcalls()

    # Warn about various stuff
    for table in cfg.tables:
        if not table in TABLE_MAP:
            # Warn about new tables in cache which are still not described by table map
            print "Warning: unmapped table {0} found in cache".format(table)
    for table in TABLE_MAP:
        if not table in cfg.tables and not table in CUSTOM_CALLS:
            # Warn about mapped tables which are missing in cache
            print "Warning: mapped table {0} cannot be found in cache".format(table)
        if not table in TABLE_ORDER and TABLE_MAP[table] is not None:
            # Warn about mapped tables not specified in processing order
            print "Warning: mapped table {0} is missing in processing order".format(table)
    for table in TABLE_ORDER:
        if not table in TABLE_MAP:
            # Warn about unmapped tables in processing order
            print "Warning: unmapped table {0} is specified in processing order".format(table)

    # Get data from reverence and write it
    for tablename in TABLE_ORDER:
        tableclass = TABLE_MAP[tablename]
        if tableclass is not None:
            # Print currently processed table name
            print "Processing: {0}".format(tablename)
            # Get table object from the Reverence and process it
            source_table = getattr(cfg, tablename) if tablename not in CUSTOM_CALLS else CUSTOM_CALLS[tablename]
            # Gather data regarding columns for current table in cache and eos
            cols_eos = set(prop.key for prop in class_mapper(TABLE_MAP[tablename]).iterate_properties if isinstance(prop, ColumnProperty))
            cols_rev = set(get_source_headers(source_table))
            notineos = cols_rev.difference(cols_eos)
            notinrev = cols_eos.difference(cols_rev)
            if notineos:
                print "Warning: {0} found in cache but missing in eos definitions: {1}".format("column" if len(notineos) == 1 else "columns", ", ".join(sorted(notineos)))
            if notinrev:
                print "Warning: {0} found in eos definitions but missing in cache: {1}".format("column" if len(notinrev) == 1 else "columns", ", ".join(sorted(notinrev)))
            process_table(source_table, tablename, tableclass)
