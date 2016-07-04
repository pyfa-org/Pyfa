# remoteWebifierFalloff
#
# Used by:
# Modules from group: Stasis Grappler (7 of 7)
# Modules from group: Stasis Web (18 of 18)
type = "active", "projected"
def handler(fit, module, context):
    if "projected" not in context: return
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties = True, remoteResists=True)


# TODO
# believe this doesn't actual require skills to use.
# Need to figure out how to remove the skill req *OR* tie it to the structure.