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

from enum import Enum, IntEnum, unique, auto


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
    Contains different types of items for multibuy export
    """
    IMPLANTS = 1
    CARGO = 2
    LOADED_CHARGES = 3
    OPTIMIZE_PRICES = 4


@unique
class PortEftOptions(IntEnum):
    """
    Contains different options for eft-export
    """
    IMPLANTS = 1
    MUTATIONS = 2
    LOADED_CHARGES = 3


@unique
class PortEftRigSize(IntEnum):
    """
    Contains different sizes of ship rigs
    This enum is not actively used, but maybe useful someday.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    CAPITAL = 4


@unique
class PortDnaOptions(IntEnum):
    """
    Contains different types of items for DNA export
    """
    FORMATTING = 1


@unique
class GuiAttrGroup(IntEnum):
    """
    Define the various groups of attributes.
    This enum is used for GUI functions and getting redefined in
    /gui/builtinItemStatsViews/attributeGrouping.py
    """
    FITTING = auto()
    STRUCTURE = auto()
    SHIELD = auto()
    ARMOR = auto()
    TARGETING = auto()
    EWAR_RESISTS = auto()
    CAPACITOR = auto()
    SHARED_FACILITIES = auto()
    FIGHTER_FACILITIES = auto()
    ON_DEATH = auto()
    JUMP_SYSTEMS = auto()
    PROPULSIONS = auto()
    FIGHTERS = auto()
    SHIP_GROUP = auto()


@unique
class GraphDpsDroneMode(IntEnum):
    auto = 1
    followAttacker = 2
    followTarget = 3


@unique
class GraphCacheCleanupReason(IntEnum):
    fitChanged = auto()
    fitRemoved = auto()
    profileChanged = auto()
    profileRemoved = auto()
    graphSwitched = auto()
    inputChanged = auto()
    optionChanged = auto()
