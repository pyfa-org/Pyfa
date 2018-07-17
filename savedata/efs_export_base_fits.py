import inspect
import os
import platform
import re
import sys
import traceback
from optparse import AmbiguousOptionError, BadOptionError, OptionParser

from logbook import CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger, NestedSetup, NullHandler, StreamHandler, TimedRotatingFileHandler, WARNING, \
    __version__ as logbook_version

sys.path.append(os.getcwd())
import config

from math import log

try:
    import wxversion
except ImportError:
    wxversion = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

pyfalog = Logger(__name__)

class PassThroughOptionParser(OptionParser):

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)

usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-w", "--wx28", action="store_true", dest="force28", help="Force usage of wxPython 2.8", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)
parser.add_option("-t", "--title", action="store", dest="title", help="Set Window Title", default=None)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)
parser.add_option("-l", "--logginglevel", action="store", dest="logginglevel", help="Set desired logging level [Critical|Error|Warning|Info|Debug]", default="Error")

(options, args) = parser.parse_args()

if options.rootsavedata is True:
    config.saveInRoot = True

config.debug = options.debug

config.defPaths(options.savepath)

try:
    import requests
    config.requestsVersion = requests.__version__
except ImportError:
    raise PreCheckException("Cannot import requests. You can download requests from https://pypi.python.org/pypi/requests.")

import eos.db

#if config.saVersion[0] > 0 or config.saVersion[1] >= 7:
    # <0.7 doesn't have support for events ;_; (mac-deprecated)
config.sa_events = True
import eos.events

    # noinspection PyUnresolvedReferences
import service.prefetch  # noqa: F401

        # Make sure the saveddata db exists
if not os.path.exists(config.savePath):
    os.mkdir(config.savePath)

eos.db.saveddata_meta.create_all()

import json
from service.fit import Fit
from service.efsPort import EfsPort

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relation, mapper, synonym, deferred
from eos.db import gamedata_session
from eos.db import gamedata_meta
from eos.db.gamedata.metaGroup import metatypes_table, items_table
from eos.db.gamedata.group import groups_table

from eos.gamedata import AlphaClone, Attribute, Category, Group, Item, MarketGroup, \
    MetaGroup, AttributeInfo, MetaData, Effect, ItemEffect, Traits
from eos.db.gamedata.traits import traits_table
from eos.saveddata.mode import Mode

def exportBaseShips(opts):
    nameReq = ''
    if opts:
        if opts.search:
            nameReq = opts.search
        if opts.outputpath:
            basePath = opts.outputpath
        elif opts.savepath:
            basePath = opts.savepath
        else:
            basePath = config.savePath + os.sep
    else:
        basePath = config.savePath + os.sep
    if basePath[len(basePath) - 1] != os.sep:
        basePath = basePath + os.sep
    outputBaseline = open(basePath + 'shipBaseJSON.js', 'w')
    outputBaseline.write('let shipBaseJSON = JSON.stringify([')
    shipCata = eos.db.getItemsByCategory('Ship')
    baseLimit = 1000
    baseN = 0
    for ship in iter(shipCata):
        if baseN < baseLimit and nameReq in ship.name:
            print(ship.name)
            print(ship.groupID)
            dna = str(ship.ID)
            if ship.groupID == 963:
                stats = t3cGetStatSet(dna, ship.name, ship.groupID, ship.raceID)
            elif ship.groupID == 1305:
                stats = t3dGetStatSet(dna, ship.name, ship.groupID, ship.raceID)
            else:
                stats = setFitFromString(dna, ship.name, ship.groupID)
            outputBaseline.write(stats)
            outputBaseline.write(',\n')
            baseN += 1
    outputBaseline.write(']);\nexport {shipBaseJSON};')
    outputBaseline.close()

def t3dGetStatSet(dnaString, shipName, groupID, raceID):
    t3dModeGroupFilter = Group.groupID == 1306
    data = list(gamedata_session.query(Group).options().filter(t3dModeGroupFilter).all())
    #Normally we would filter this via the raceID,
    #Unfortunately somebody fat fingered the Jackdaw modes raceIDs as 4 (Amarr) not 1 (Caldari)
    # t3dModes = list(filter(lambda mode: mode.raceID == raceID, data[0].items)) #Line for if/when they fix it
    t3dModes = list(filter(lambda mode: shipName in mode.name, data[0].items))
    shipModeData = ''
    n = 0
    while n < len(t3dModes):
        dna = dnaString + ':' + str(t3dModes[n].ID) + ';1'
        #Don't add the new line for the last mode
        if n < len(t3dModes) - 1:
            shipModeData += setFitFromString(dna, t3dModes[n].name, groupID) + ',\n'
        else:
            shipModeData += setFitFromString(dna, t3dModes[n].name, groupID)
        n += 1
    return shipModeData

def t3cGetStatSet(dnaString, shipName, groupID, raceID):
    subsystemFilter = Group.categoryID == 32
    data = list(gamedata_session.query(Group).options().filter(subsystemFilter).all())
    # multi dimension array to hold the t3c subsystems as ss[index of subsystem type][index subsystem item]
    ss = [[], [], [], []]
    s = 0
    while s < 4:
        ss[s] = list(filter(lambda subsystem: subsystem.raceID == raceID, data[s].items))
        s += 1
    print(shipName)
    print(ss)
    shipPermutationData = ''
    n = 0
    a = 0
    while a < 3:
        b = 0
        while b < 3:
            c = 0
            while c < 3:
                d = 0
                while d < 3:
                    dna = dnaString + ':' + str(ss[0][a].ID) \
                          + ';1:' + str(ss[1][b].ID) + ';1:' + str(ss[2][c].ID) \
                          + ';1:' + str(ss[3][d].ID) + ';1'
                    #Don't add the new line for the last permutation
                    if a == 2 and b == 2 and c == 2 and d == 2:
                        shipPermutationData += setFitFromString(dna, shipName, groupID)
                    else:
                        shipPermutationData += setFitFromString(dna, shipName, groupID) + ',\n'
                    d += 1
                    n += 1
                c += 1
            b += 1
        a += 1
    print(str(n) + ' subsystem conbinations for ' + shipName)
    return shipPermutationData
try:
    armorLinkShip = eos.db.searchFits('armor links')[0]
    infoLinkShip = eos.db.searchFits('information links')[0]
    shieldLinkShip =  eos.db.searchFits('shield links')[0]
    skirmishLinkShip = eos.db.searchFits('skirmish links')[0]
except:
    armorLinkShip = None
    infoLinkShip = None
    shieldLinkShip = None
    skirmishLinkShip = None

def setFitFromString(dnaString, fitName, groupID) :
    if armorLinkShip == None:
        print('Cannot find correct link fits for base calculations')
        return ''
    modArray = dnaString.split(':')
    fitL = Fit()
    fitID = fitL.newFit(int(modArray[0]), fitName)
    fit = eos.db.getFit(fitID)
    ammoArray = []
    n = -1
    for mod in iter(modArray):
        n = n + 1
        if n > 0:
            modSp = mod.split(';')
            if len(modSp) == 2:
                k = 0
                while k < int(modSp[1]):
                    k = k + 1
                    itemID = int(modSp[0])
                    item = eos.db.getItem(int(modSp[0]), eager=("attributes", "group.category"))
                    cat = item.category.name
                    print(cat)
                    if cat == 'Drone':
                        fitL.addDrone(fitID, itemID, int(modSp[1]), recalc=False)
                        k += int(modSp[1])
                    if cat == 'Fighter':
                        fitL.addFighter(fitID, itemID, recalc=False)
                        k += 100
                    if fitL.isAmmo(int(modSp[0])):
                        k += 100
                        ammoArray.append(int(modSp[0]));
                    # Set mode if module is a mode on a t3d
                    if item.groupID == 1306 and groupID == 1305:
                        fitL.setMode(fitID, Mode(item))
                    else:
                        fitL.appendModule(fitID, int(modSp[0]))
    fit = eos.db.getFit(fitID)
    for ammo in iter(ammoArray):
        fitL.setAmmo(fitID, ammo, list(filter(lambda mod: str(mod).find('name') > 0, fit.modules)))
    if len(fit.drones) > 0:
        fit.drones[0].amountActive = fit.drones[0].amount
        eos.db.commit()
    for fighter in iter(fit.fighters):
        for ability in fighter.abilities:
            if ability.effect.handlerName == u'fighterabilityattackm' and ability.active == True:
                for abilityAltRef in fighter.abilities:
                    if abilityAltRef.effect.isImplemented:
                        abilityAltRef.active = True
    fitL.recalc(fit)
    fit = eos.db.getFit(fitID)
    print(list(filter(lambda mod: mod.item and mod.item.groupID in [1189, 658], fit.modules)))
    fitL.addCommandFit(fit.ID, armorLinkShip)
    fitL.addCommandFit(fit.ID, shieldLinkShip)
    fitL.addCommandFit(fit.ID, skirmishLinkShip)
    fitL.addCommandFit(fit.ID, infoLinkShip)
    jsonStr = EfsPort.exportEfs(fit, groupID)
    Fit.deleteFit(fitID)
    return jsonStr
