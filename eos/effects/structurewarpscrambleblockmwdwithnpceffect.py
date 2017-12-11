# Not used by any item
from eos.saveddata.module import State

# Not used by any item
runTime = "early"
type = "projected", "active"


def handler(fit, module, context):
    if "projected" not in context:
        return

    fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))

    # this is such a dirty hack
    for mod in fit.modules:
        if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
            mod.state = State.ONLINE
