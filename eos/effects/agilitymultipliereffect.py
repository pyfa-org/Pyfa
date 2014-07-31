# Used by:
# Modules from group: Inertia Stabilizer (12 of 12)
# Modules from group: Nanofiber Internal Structure (14 of 14)
# Modules from group: Reinforced Bulkhead (12 of 12)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("agility",
                           module.getModifiedItemAttr("agilityMultiplier"),
                           stackingPenalties = True)
