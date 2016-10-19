# shipBonusRepairSystemsArmorRepairAmountGB2
#
# Used by:
# Ship: Hyperion
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGB2"),
                                  skill="Gallente Battleship")
