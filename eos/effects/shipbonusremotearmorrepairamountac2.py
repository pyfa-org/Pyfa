# shipBonusRemoteArmorRepairAmountAC2
#
# Used by:
# Ship: Augoror
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
