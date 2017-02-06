# shipBonusDroneDamageMultiplierAD1
#
# Used by:
# Variations of ship: Dragoon (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                 src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
