# =============================================================================
# Copyright (C) 2019 Ryan Holmes
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

from eos.enum import Enum
from enum import IntEnum,unique

class FittingSlot(Enum):
    """
    Contains slots for ship fittings
    """
    # These are self-explanatory
    LOW = 1
    MED = 2
    HIGH = 3
    RIG = 4
    SUBSYSTEM = 5
    # not a real slot, need for pyfa display rack separation
    MODE = 6
    # system effects. They are projected "modules" and pyfa assumes all modules
    # have a slot. In this case, make one up.
    SYSTEM = 7
    # used for citadel services
    SERVICE = 8
    # fighter 'slots'. Just easier to put them here...
    F_LIGHT = 10
    F_SUPPORT = 11
    F_HEAVY = 12
    # fighter 'slots' (for structures)
    FS_LIGHT = 13
    FS_SUPPORT = 14
    FS_HEAVY = 15

@unique
class ImplantLocation(IntEnum):
    """
    Contains location of the implant
    """
    FIT = 0
    CHARACTER = 1

@unique
class CalcType(IntEnum):
    """
    Contains location of the calculation
    """
    LOCAL = 0
    PROJECTED = 1
    COMMAND = 2

@unique
class FittingModuleState(IntEnum):
    """
    Contains the state of a fitting module
    """
    OFFLINE = -1
    ONLINE = 0
    ACTIVE = 1
    OVERHEATED = 2

@unique
class FittingHardpoint(IntEnum):
    """
    Contains the types of a fitting hardpoint
    """
    NONE = 0
    MISSILE = 1
    TURRET = 2

@unique
class EsiLoginMethod(IntEnum):
    """
    Contains the method of ESI login
    """
    SERVER = 0
    MANUAL = 1

@unique
class EsiSsoMode(IntEnum):
    """
    Contains the mode of ESI sso mode
    """
    AUTO = 0
    CUSTOM = 1

class EsiEndpoints(Enum):
    """
    Contains the endpoint paths for the ESI access
    """
    CHAR = "/v4/characters/{character_id}/"
    CHAR_SKILLS = "/v4/characters/{character_id}/skills/"
    CHAR_FITTINGS = "/v1/characters/{character_id}/fittings/"
    CHAR_DEL_FIT = "/v1/characters/{character_id}/fittings/{fitting_id}/"

@unique
class PortMultiBuyOptions(IntEnum):
    """
    Contains different types of items to multibuy export
    """
    IMPLANTS = 1
    CARGO = 2
    LOADED_CHARGES = 3

@unique
class PortEftOptions(IntEnum):
    """
    Contains different options for eft-export
    """
    IMPLANTS = 1
    MUTATIONS = 2
    LOADED_CHARGES = 3

class PortEftRigSize(Enum):
    """
    Contains different sizes of ship rigs
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    CAPITAL = 4
