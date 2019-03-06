from eos.enum import Enum
from enum import IntEnum


class Slot(Enum):
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


class ImplantLocation(Enum):
    FIT = 0
    CHARACTER = 1


class CalcType(Enum):
    LOCAL = 0
    PROJECTED = 1
    COMMAND = 2

class State(Enum):
    OFFLINE = -1
    ONLINE = 0
    ACTIVE = 1
    OVERHEATED = 2

class Hardpoint(Enum):
    NONE = 0
    MISSILE = 1
    TURRET = 2

class LoginMethod(Enum):
    SERVER = 0
    MANUAL = 1

class SsoMode(Enum):
    AUTO = 0
    CUSTOM = 1

class ESIEndpoints(Enum):
    CHAR = "/v4/characters/{character_id}/"
    CHAR_SKILLS = "/v4/characters/{character_id}/skills/"
    CHAR_FITTINGS = "/v1/characters/{character_id}/fittings/"
    CHAR_DEL_FIT = "/v1/characters/{character_id}/fittings/{fitting_id}/"

class MultiBuy_ItemType(IntEnum):
    IMPLANTS = 1
    CARGO = 2
    LOADED_CHARGES = 3

class Options(IntEnum):
    IMPLANTS = 1
    MUTATIONS = 2
    LOADED_CHARGES = 3

class RigSize(Enum):
    # Matches to item attribute "rigSize" on ship and rig items
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    CAPITAL = 4
