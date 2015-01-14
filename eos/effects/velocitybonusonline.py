# velocityBonusOnline
#
# Used by:
# Modules from group: Nanofiber Internal Structure (7 of 7)
# Modules from group: Overdrive Injector System (7 of 7)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("implantBonusVelocity"),
                           stackingPenalties = True)