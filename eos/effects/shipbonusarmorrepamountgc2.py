# shipBonusArmorRepAmountGC2
#
# Used by:
# Ship: Deimos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGC2"),
                                  skill="Gallente Cruiser")
