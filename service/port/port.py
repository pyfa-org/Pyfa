# =============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import re
import os
import threading
import xml.dom
import xml.parsers.expat
from codecs import open

from bs4 import UnicodeDammit
from logbook import Logger

from eos import db
from eos.const import ImplantLocation
from service.fit import Fit as svcFit
from service.port.dna import exportDna, importDna, importDnaAlt
from service.port.eft import (
    exportEft, importEft, importEftCfg,
    isValidDroneImport, isValidFighterImport, isValidCargoImport,
    isValidImplantImport, isValidBoosterImport)
from service.port.esi import exportESI, importESI
from service.port.multibuy import exportMultiBuy
from service.port.shipstats import exportFitStats
from service.port.xml import importXml, exportXml
from service.port.muta import parseMutant, parseDynamicItemString, fetchDynamicItem


pyfalog = Logger(__name__)

# 2017/04/05 NOTE: simple validation, for xml file
RE_XML_START = r'<\?xml\s+version="1.0"[^<>]*\?>'


class Port:
    """Service which houses all import/export format functions"""
    instance = None
    __tag_replace_flag = True

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Port()

        return cls.instance

    @classmethod
    def set_tag_replace(cls, b):
        cls.__tag_replace_flag = b

    @classmethod
    def is_tag_replace(cls):
        # might there is a person who wants to hold tags.
        # (item link in EVE client etc. When importing again to EVE)
        return cls.__tag_replace_flag

    @staticmethod
    def backupFits(path, progress):
        pyfalog.debug("Starting backup fits thread.")

        def backupFitsWorkerFunc(path, progress):
            try:
                backedUpFits = Port.exportXml(svcFit.getInstance().getAllFits(), progress)
                if backedUpFits:
                    progress.message = f'writing {path}'
                    backupFile = open(path, "w", encoding="utf-8")
                    backupFile.write(backedUpFits)
                    backupFile.close()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                progress.error = f'{e}'
            finally:
                progress.current += 1
                progress.workerWorking = False

        threading.Thread(
            target=backupFitsWorkerFunc,
            args=(path, progress)
        ).start()

    @staticmethod
    def importFitsThreaded(paths, progress):
        """
        :param paths: fits data file path list.
        :rtype: None
        """
        pyfalog.debug("Starting import fits thread.")

        def importFitsFromFileWorkerFunc(paths, progress):
            Port.importFitFromFiles(paths, progress)

        threading.Thread(
            target=importFitsFromFileWorkerFunc,
            args=(paths, progress)
        ).start()

    @staticmethod
    def importFitFromFiles(paths, progress=None):
        """
        Imports fits from file(s). First processes all provided paths and stores
        assembled fits into a list. This allows us to call back to the GUI as
        fits are processed as well as when fits are being saved.
        returns
        """

        sFit = svcFit.getInstance()

        fit_list = []
        try:
            for path in paths:
                if progress:
                    if progress and progress.userCancelled:
                        progress.workerWorking = False
                        return False, "Cancelled by user"
                    msg = "Processing file:\n%s" % path
                    progress.message = msg
                    pyfalog.debug(msg)

                with open(path, "rb") as file_:
                    srcString = file_.read()
                    dammit = UnicodeDammit(srcString)
                    srcString = dammit.unicode_markup

                if len(srcString) == 0:  # ignore blank files
                    pyfalog.debug("File is blank.")
                    continue

                try:
                    importType, makesNewFits, fitsImport = Port.importAuto(srcString, path, progress=progress)
                    fit_list += fitsImport
                except xml.parsers.expat.ExpatError:
                    pyfalog.warning("Malformed XML in:\n{0}", path)
                    msg = "Malformed XML in %s" % path
                    if progress:
                        progress.error = msg
                        progress.workerWorking = False
                    return False, msg

            numFits = len(fit_list)
            for idx, fit in enumerate(fit_list):
                if progress and progress.userCancelled:
                    progress.workerWorking = False
                    return False, "Cancelled by user"
                # Set some more fit attributes and save
                fit.character = sFit.character
                fit.damagePattern = sFit.pattern
                fit.targetProfile = sFit.targetProfile
                if len(fit.implants) > 0:
                    fit.implantLocation = ImplantLocation.FIT
                else:
                    useCharImplants = sFit.serviceFittingOptions["useCharacterImplantsByDefault"]
                    fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
                db.save(fit)
                # IDs.append(fit.ID)
                if progress:
                    pyfalog.debug("Processing complete, saving fits to database: {0}/{1}", idx + 1, numFits)
                    progress.message = "Processing complete, saving fits to database\n(%d/%d) %s" % (idx + 1, numFits, fit.ship.name)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            pyfalog.critical("Unknown exception processing: {0}", paths)
            pyfalog.critical(e)
            if progress:
                progress.error = f'{e}'
                progress.workerWorking = False
            return False, "Unknown error while processing {}\n\n Error: {} {}".format(
                paths, type(e).__name__, getattr(e, 'message', ''))

        if progress:
            progress.cbArgs.append(fit_list[:])
            progress.workerWorking = False
        return True, fit_list

    @staticmethod
    def importFitFromBuffer(bufferStr, activeFit=None):
        # type: (str, object) -> object
        # TODO: catch the exception?
        # activeFit is reserved?, bufferStr is unicode? (assume only clipboard string?
        sFit = svcFit.getInstance()
        importType, makesNewFits, importData = Port.importAuto(bufferStr, activeFit=activeFit)

        if makesNewFits:
            for fit in importData:
                fit.character = sFit.character
                fit.damagePattern = sFit.pattern
                fit.targetProfile = sFit.targetProfile
                if len(fit.implants) > 0:
                    fit.implantLocation = ImplantLocation.FIT
                else:
                    useCharImplants = sFit.serviceFittingOptions["useCharacterImplantsByDefault"]
                    fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
                db.save(fit)
        return importType, importData

    @classmethod
    def importAuto(cls, string, path=None, activeFit=None, progress=None):
        lines = string.splitlines()
        # Get first line and strip space symbols of it to avoid possible detection errors
        firstLine = ''
        for line in lines:
            line = line.strip()
            if line:
                firstLine = line
                break

        # If XML-style start of tag encountered, detect as XML
        if re.search(RE_XML_START, firstLine):
            return "XML", True, cls.importXml(string, progress)

        # If JSON-style start, parse as CREST/JSON
        if firstLine[0] == '{':
            return "JSON", True, (cls.importESI(string),)

        # If we've got source file name which is used to describe ship name
        # and first line contains something like [setup name], detect as eft config file
        if re.match("^\s*\[.*\]", firstLine) and path is not None:
            filename = os.path.split(path)[1]
            shipName = filename.rsplit('.')[0]
            return "EFT Config", True, cls.importEftCfg(shipName, lines, progress)

        # If no file is specified and there's comma between brackets,
        # consider that we have [ship, setup name] and detect like eft export format
        if re.match("^\s*\[.*,.*\]", firstLine):
            return "EFT", True, (cls.importEft(lines),)

        # Check if string is in DNA format
        dnaPattern = "\d+(:\d+(;\d+))*::"
        if re.match(dnaPattern, firstLine):
            return "DNA", True, (cls.importDna(string),)
        dnaChatPattern = "<url=fitting:(?P<dna>{})>(?P<fitName>[^<>]+)</url>".format(dnaPattern)
        m = re.search(dnaChatPattern, firstLine)
        if m:
            return "DNA", True, (cls.importDna(m.group("dna"), fitName=m.group("fitName")),)
        m = re.search(r"DNA:(?P<dna>\d+(:\d+(\*\d+)?)*)", firstLine)
        if m:
            return "DNA", True, (cls.importDnaAlt(m.group("dna")),)

        if activeFit is not None:

            # Try to import mutated item from network
            dynData = parseDynamicItemString(string)
            if dynData is not None:
                itemData = fetchDynamicItem(dynData)
                if itemData is not None:
                    baseItem, mutaplasmidItem, mutations = itemData
                    return "FittingItem", False, ((baseItem, mutaplasmidItem, mutations),)

            # Try to import mutated module
            try:
                baseItem, mutaplasmidItem, mutations = parseMutant(lines)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pass
            else:
                if baseItem is not None:
                    return "FittingItem", False, ((baseItem, mutaplasmidItem, mutations),)
            # Try to import into one of additions panels
            isDrone, droneData = isValidDroneImport(string)
            if isDrone:
                return "AdditionsDrones", False, (droneData,)
            isFighter, fighterData = isValidFighterImport(string)
            if isFighter:
                return "AdditionsFighters", False, (fighterData,)
            isImplant, implantData = isValidImplantImport(string)
            if isImplant:
                return "AdditionsImplants", False, (implantData,)
            isBooster, boosterData = isValidBoosterImport(string)
            if isBooster:
                return "AdditionsBoosters", False, (boosterData,)
            isCargo, cargoData = isValidCargoImport(string)
            if isCargo:
                return "AdditionsCargo", False, (cargoData,)

    # EFT-related methods
    @staticmethod
    def importEft(lines):
        return importEft(lines)

    @staticmethod
    def importEftCfg(shipname, lines, progress=None):
        return importEftCfg(shipname, lines, progress)

    @classmethod
    def exportEft(cls, fit, options, callback=None):
        return exportEft(fit, options, callback=callback)

    # DNA-related methods
    @staticmethod
    def importDna(string, fitName=None):
        return importDna(string, fitName=fitName)

    @staticmethod
    def importDnaAlt(string, fitName=None):
        return importDnaAlt(string, fitName=fitName)

    @staticmethod
    def exportDna(fit, options, callback=None):
        return exportDna(fit, options, callback=callback)

    # ESI-related methods
    @staticmethod
    def importESI(string):
        return importESI(string)

    @staticmethod
    def exportESI(fit, exportCharges, exportImplants, exportBoosters, callback=None):
        return exportESI(fit, exportCharges, exportImplants, exportBoosters, callback=callback)

    # XML-related methods
    @staticmethod
    def importXml(text, progress=None):
        return importXml(text, progress)

    @staticmethod
    def exportXml(fits, progress=None, callback=None):
        return exportXml(fits, progress, callback=callback)

    # Multibuy-related methods
    @staticmethod
    def exportMultiBuy(fit, options, callback=None):
        return exportMultiBuy(fit, options, callback=callback)

    @staticmethod
    def exportFitStats(fit, callback=None):
        return exportFitStats(fit, callback=callback)
