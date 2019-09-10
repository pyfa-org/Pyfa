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

from enum import IntEnum,unique


@unique
class FittingSlot(IntEnum):
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
class SpoolType(IntEnum):
    # Spool and cycle scale are different in case if max spool amount cannot
    # be divided by spool step without remainder
    SPOOL_SCALE = 0  # [0..1]
    CYCLE_SCALE = 1  # [0..1]
    TIME = 2  # Expressed via time in seconds since spool up started
    CYCLES = 3  # Expressed in amount of cycles since spool up started


@unique
class FitSystemSecurity(IntEnum):
    HISEC = 0
    LOWSEC = 1
    NULLSEC = 2
    WSPACE = 3


@unique
class Operator(IntEnum):
    PREASSIGN = 0
    PREINCREASE = 1
    MULTIPLY = 2
    POSTINCREASE = 3
    FORCE = 4
