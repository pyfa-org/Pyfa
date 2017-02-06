# agilityMultiplierEffect
#
# Used by:
# Modules from group: Inertial Stabilizer (7 of 7)
# Modules from group: Nanofiber Internal Structure (7 of 7)
# Modules from group: Reinforced Bulkhead (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility",
                           module.getModifiedItemAttr("agilityMultiplier"),
                           stackingPenalties=True)
