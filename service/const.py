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

from enum import Enum, IntEnum, unique, auto as autoId


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
    CHAR = "/v5/characters/{character_id}/"
    CHAR_SKILLS = "/v4/characters/{character_id}/skills/"
    CHAR_FITTINGS = "/v1/characters/{character_id}/fittings/"
    CHAR_DEL_FIT = "/v1/characters/{character_id}/fittings/{fitting_id}/"
    DYNAMIC_ITEM = "/v1/dogma/dynamic/items/{type_id}/{item_id}/"


@unique
class PortMultiBuyOptions(IntEnum):
    """
    Contains different types of items for multibuy export
    """
    IMPLANTS = 1
    CARGO = 2
    LOADED_CHARGES = 3
    OPTIMIZE_PRICES = 4
    BOOSTERS = 5


@unique
class PortEftOptions(IntEnum):
    """
    Contains different options for eft-export
    """
    IMPLANTS = 1
    MUTATIONS = 2
    LOADED_CHARGES = 3
    CARGO = 4
    BOOSTERS = 5


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
    FITTING = autoId()
    STRUCTURE = autoId()
    SHIELD = autoId()
    ARMOR = autoId()
    TARGETING = autoId()
    EWAR_RESISTS = autoId()
    CAPACITOR = autoId()
    SHARED_FACILITIES = autoId()
    FIGHTER_FACILITIES = autoId()
    ON_DEATH = autoId()
    JUMP_SYSTEMS = autoId()
    PROPULSIONS = autoId()
    FIGHTERS = autoId()
    SHIP_GROUP = autoId()


@unique
class GraphDpsDroneMode(IntEnum):
    auto = 1
    followAttacker = 2
    followTarget = 3


@unique
class GraphCacheCleanupReason(IntEnum):
    fitChanged = autoId()
    fitRemoved = autoId()
    profileChanged = autoId()
    profileRemoved = autoId()
    graphSwitched = autoId()
    inputChanged = autoId()
    optionChanged = autoId()
    resistModeChanged = autoId()
    hpEffectivityChanged = autoId()


@unique
class TargetResistMode(IntEnum):
    auto = autoId()
    shield = autoId()
    armor = autoId()
    hull = autoId()
    weightedAverage = autoId()


@unique
class GraphColor(IntEnum):
    red = autoId()
    green = autoId()
    blue = autoId()
    yellow = autoId()
    cyan = autoId()
    magenta = autoId()
    orange = autoId()
    purple = autoId()


@unique
class GraphLightness(IntEnum):
    normal = autoId()
    dark = autoId()
    bright = autoId()


@unique
class GraphLineStyle(IntEnum):
    solid = autoId()
    dashed = autoId()
    dotted = autoId()
    dashdotted = autoId()
