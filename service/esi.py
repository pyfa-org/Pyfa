# noinspection PyPackageRequirements
import wx
from logbook import Logger
import threading
import copy
import uuid
import time

import eos.db
from eos.enum import Enum
from eos.saveddata.ssocharacter import CrestChar
import gui.globalEvents as GE
from service.settings import CRESTSettings
from service.server import StoppableHTTPServer, AuthHandler
from service.pycrest.eve import EVE

pyfalog = Logger(__name__)


class Servers(Enum):
    TQ = 0
    SISI = 1


class CrestModes(Enum):
    IMPLICIT = 0
    USER = 1


class ESI(object):
    # @todo: move this to settings
    clientCallback = 'http://localhost:6461'
    clientTest = True

    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = ESI()

        return cls._instance


    def __init__(self):
        pass
