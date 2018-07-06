from optparse import AmbiguousOptionError, BadOptionError, OptionParser

class PassThroughOptionParser(OptionParser):

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)

usage = "usage: %prog [options]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option(
    "-f", "--exportfits", action="store_true", dest="exportfits", \
    help="Export this copy of pyfa's local fits to a shipJSON file that Eve Fleet Simulator can import from", \
    default=False)
parser.add_option(
    "-b", "--exportbaseships", action="store_true", dest="exportbaseships", \
    help="Export ship stats to a shipBaseJSON file used by Eve Fleet Simulator", \
    default=False)
parser.add_option(
    "-c", "--convertfitsfromhtml", action="store_true", dest="convertfitsfromhtml", \
    help="Convert an exported pyfaFits.html file to a shipJSON file that Eve Fleet Simulator can import from\n"
    + "    Note this process loses data like fleet boosters as the DNA format exported by to html contains limited data", \
    default=False)
parser.add_option("-s", "--savepath", action="store", dest="savepath",
                  help="Set the folder for savedata", default=None)
parser.add_option(
    "-o", "--outputpath", action="store", dest="outputpath",
    help="Output directory, defaults to the savepath", default=None)
parser.add_option(
    '-i', "--search", action="store", dest="search",
    help="Ignore ships and fits that don't contain the searched string", default=None)


(options, args) = parser.parse_args()

if options.exportfits:
    from efs_export_pyfa_fits import exportPyfaFits
    exportPyfaFits(options)

if options.exportbaseships:
    from efs_export_base_fits import exportBaseShips
    exportBaseShips(options)

if options.convertfitsfromhtml:
    from efs_process_html_export import efsFitsFromHTMLExport
    efsFitsFromHTMLExport(options)

#stuff bellow this point is purely scrap diagnostic stuff and should not be public (as it's scrawl)
def printGroupData():
    from eos.db import gamedata_session
    from eos.gamedata import Group, Category
    filterVal = Group.categoryID == 6
    data = gamedata_session.query(Group).options().list(filter(filterVal).all())
    for group in data:
        print(group.groupName + '  groupID: ' + str(group.groupID))
    return ''

def printSizeData():
    from eos.db import gamedata_session
    from eos.gamedata import Group
    filterVal = Group.categoryID == 6
    data = gamedata_session.query(Group).options().filter(filterVal).all()
    ships = gamedata_session.query(Group).options().filter(filterVal)
    print(data)
    print(vars(data[0]))

    shipSizes = ['Frigate', 'Destroyer', 'Cruiser', 'Battlecruiser', 'Battleship', 'Capital', 'Industrial', 'Misc']
    groupSets = [
        [25, 31, 237, 324, 830, 831, 834, 893, 1283, 1527],
        [420, 541, 1305, 1534],
        [26, 358, 832, 833, 894, 906, 963],
        [419, 540, 1201],
        [27, 381, 898, 900],
        [30, 485, 513, 547, 659, 883, 902, 1538],
        [28, 380, 1202, 463, 543, 941],
        [29, 1022]
    ]
    i = 0
    while i < 8:
        groupNames = '\'' + shipSizes[i] + '\': {\'name\': \'' + shipSizes[i] + '\', \'groupIDs\': groupIDFromGroupName(['
        for gid in groupSets[i]:
            if gid is not groupSets[i][0]:
                groupNames = groupNames + '\', '
            groupNames = groupNames + '\'' + list(filter(lambda gr: gr.groupID == gid, data))[0].groupName
        print(groupNames + '\'], data)}')
        i = i + 1
    projectedModGroupIds = [
        41, 52, 65, 67, 68, 71, 80, 201, 208, 291, 325, 379, 585,
        842, 899, 1150, 1154, 1189, 1306, 1672, 1697, 1698, 1815, 1894
    ]
    from eos.db import gamedata_session
    from eos.gamedata import Group
    data = gamedata_session.query(Group).all()
    groupNames = ''
    for gid in projectedModGroupIds:
        if gid is not projectedModGroupIds[0]:
            groupNames = groupNames + '\', '
        print(gid)
        groupNames = groupNames + '\'' + list(filter(lambda gr: gr.groupID == gid, data))[0].groupName
    print(groupNames + '\'')

def wepMultisFromTraitText(fit):
    filterVal = Traits.typeID == fit.shipID
    data = gamedata_session.query(Traits).options().filter(filterVal).all()
    roleBonusMode = False
    if len(data) == 0:
        return multipliers
    d = data[0]
    s1 = str(vars(d))
    ds = s1.encode(encoding="utf-8", errors="ignore")
    #print(ds)
    previousTypedBonus = 0
    previousDroneTypeBonus = 0
    for bonusText in data[0].traitText.splitlines():
        bonusText = bonusText.lower()
        if 'per skill level' in bonusText:
            roleBonusMode = False
        if 'role bonus' in bonusText or 'misc bonus' in bonusText:
            roleBonusMode = True
        multi = 1
        if 'damage' in bonusText and not any(e in bonusText for e in ['control', 'heat']):
            splitText = bonusText.split('%')
            if (float(splitText[0]) > 0) is False:
                print('damage bonus split did not parse correctly!')
                print(float(splitText[0]))
            if roleBonusMode:
                addedMulti = float(splitText[0])
            else:
                addedMulti = float(splitText[0]) * 5
            if any(e in bonusText for e in [' em', 'thermal', 'kinetic', 'explosive']):
                if addedMulti > previousTypedBonus:
                    previousTypedBonus = addedMulti
                else:
                    addedMulti = 0
            if any(e in bonusText for e in ['heavy drone', 'medium drone', 'light drone', 'sentry drone']):
                if addedMulti > previousDroneTypeBonus:
                    previousDroneTypeBonus = addedMulti
                else:
                    addedMulti = 0
            multi = 1 + (addedMulti / 100)
        elif 'rate of fire' in bonusText:
            splitText = bonusText.split('%')
            if (float(splitText[0]) > 0) is False:
                print('rate of fire bonus split did not parse correctly!')
                print(float(splitText[0]))
            if roleBonusMode:
                rofMulti = float(splitText[0])
            else:
                rofMulti = float(splitText[0]) * 5
            multi = 1 / (1 - (rofMulti / 100))
        if multi > 1:
            if 'drone' in bonusText.lower():
                multipliers['droneBandwidth'] *= multi
            elif 'turret' in bonusText.lower():
                multipliers['turret'] *= multi
            elif any(e in bonusText for e in ['missile', 'torpedo']):
                multipliers['launcher'] *= multi


def examDiff(ai, bi, attr=False):
    print('')
    print('A:' + str(ai))
    print('B:' + str(bi))
    a =  dict(map(lambda k: (k, getattr(ai, k)), dir(ai)))
    b = dict(map(lambda k: (k, getattr(bi, k)), dir(bi)))
    try:
        print(a.keys())
        print('A:' + str(a))
        print(b.keys())
        print('B:' + str(b))
        print('A exclusive keys:')
        for key in filter(lambda k: k not in b.keys(), a.keys()):
            print(key)
        print('B exclusive keys:')
        for key in filter(lambda k: k not in a.keys(), b.keys()):
            print(key)
        print('A key/value pairs where B is None:')
        for key in filter(lambda k: k in b.keys() and b[k] == None and a[k] != None, a.keys()):
            print(key)
            print(a[key])
        print('B key/value pairs where A is None:')
        for key in filter(lambda k: k in a.keys() and a[k] == None and b[k] != None, b.keys()):
            print(key)
            print(b[key])
    except Exception as e:
        if attr == True:
            print('Could not print itemModifiedAttributes for a or b')
            print(e)
        else:
            print('Checking itemModifiedAttributes diff')
            examDiff(ai.itemModifiedAttributes, bi.itemModifiedAttributes, True)
    if attr == False:
        print('Checking itemModifiedAttributes diff')
        examDiff(ai.itemModifiedAttributes, bi.itemModifiedAttributes, True)
    print('')

def groupIDFromGroupName(names, data=None):
    # Group data can optionally be passed to the function to improve preformace with repeated calls.
    if data is None:
        data = gamedata_session.query(Group).all()
    returnSingle = False
    if not isinstance(names, list):
        names = [names]
        returnSingle = True
    gidList = list(map(lambda incGroup: incGroup.groupID, (filter(lambda group: group.groupName in names, data))))
    if returnSingle:
        return gidList[0]
    return gidList
