# structureWarpScrambleBlockMWDWithNPCEffect
#
# Used by:
# Structure Modules from group: Structure Warp Scrambler (2 of 2)
from eos.saveddata.module import State

# Not used by any item
runTime = "early"
type = "projected", "active"


def handler(fit, module, context):
    if "projected" in context:
        fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
        if module.charge is not None and module.charge.ID == 47336:
            for mod in fit.modules:
                if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
                    mod.state = State.ONLINE
                if not mod.isEmpty and mod.item.requiresSkill("Micro Jump Drive Operation") and mod.state > State.ONLINE:
                    mod.state = State.ONLINE
