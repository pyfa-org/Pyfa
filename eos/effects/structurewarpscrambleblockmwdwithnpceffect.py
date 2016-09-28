# Not used by any item
runTime = "early"
type = "projected", "active"

from eos.types import State

def handler(fit, module, context):
    if "projected" not in context:
        return
    # this is such a dirty hack
    for mod in fit.modules:
        if not mod.isEmpty and mod.item.requiresSkill("High Speed Maneuvering") and mod.state > State.ONLINE:
            mod.state = State.ONLINE
