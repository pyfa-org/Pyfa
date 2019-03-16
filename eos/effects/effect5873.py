# shipBonusArmorRepairGI2
#
# Used by:
# Ship: Occator
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGI2"),
                                  skill="Gallente Industrial")
