# shipBonusRemoteArmorRepairAmountGF2
#
# Used by:
# Variations of ship: Navitas (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
