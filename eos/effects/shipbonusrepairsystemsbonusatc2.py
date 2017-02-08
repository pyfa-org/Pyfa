# shipBonusRepairSystemsBonusATC2
#
# Used by:
# Ship: Vangel
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusATC2"))
