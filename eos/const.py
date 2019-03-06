from eos.enum import Enum



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
