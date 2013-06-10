# Used by:
# Modules from group: Nanofiber Internal Structure (14 of 14)
# Modules from group: Overdrive Injector System (14 of 14)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("implantBonusVelocity"),
                           stackingPenalties = True)