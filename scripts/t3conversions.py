# Prints out a fucking large python dictionary for use with the t3c conversion migration.\
# Requires eve-old.db file (which is the previous releases database so that we can lookup the old items)
# See https://community.eveonline.com/news/patch-notes/patch-notes-for-july-2017-release

import sys
from os.path import realpath, join, dirname, abspath
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import csv

newDB = create_engine('sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "eve.db")), sys.getfilesystemencoding()))
oldDB = create_engine('sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "eve-old.db")), sys.getfilesystemencoding()))

oldItemMapping = {}
newItemMapping = {}

with open('t3conversionSheet.csv', 'r') as f:
    reader = csv.reader(f)
    print "conversion = {"
    for row in reader:

        fromList = []
        toList = []
        for x in xrange(1, 6):
            try:
                if (row[0], row[x]) not in oldItemMapping:
                    item = oldDB.execute("SELECT * FROM invtypes WHERE typeName LIKE ?", ("{}%{}".format(row[0], row[x]),)).first()
                    oldItemMapping[(row[0], row[x])] = item['typeID']
                fromList.append(str(oldItemMapping[(row[0], row[x])]))
            except:
                pass
        for x in xrange(6, 10):
            if row[x] not in newItemMapping:
                item = newDB.execute("SELECT * FROM invtypes WHERE typeName = ?",
                                     (row[x],)).first()
                newItemMapping[row[x]] = item['typeID']
            toList.append(str(newItemMapping[row[x]]))
        print "\tfrozenset([{}]): ({}),".format(','.join(fromList), ','.join(toList))
print "}"

with open('t3conversionSheetLoose.csv', 'r') as f:
    reader = csv.reader(f)
    print "conversion2 = {"
    for row in reader:
        oldItem = oldDB.execute("SELECT typeID FROM invtypes WHERE typeName = ?", (row[0],)).scalar()
        newItem = newDB.execute("SELECT typeID FROM invtypes WHERE typeName = ?", (row[1],)).scalar()
        print "\t{}: {},".format(oldItem, newItem)
print "}"
