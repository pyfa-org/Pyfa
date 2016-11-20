# Drone damage bonus
#
# Used by:
# Orca
type = "passive"

def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier",
                                 src.getModifiedItemAttr("industrialBonusDroneDamage"), stackingPenalties = True)

