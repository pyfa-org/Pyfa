# structureModuleEffectStasisWebifier
#
# Used by:
# Structure Modules from group: Structure Stasis Webifier (2 of 2)
type = "active", "projected"


def handler(fit, module, context, *args, **kwargs):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties=True, *args, **kwargs)
