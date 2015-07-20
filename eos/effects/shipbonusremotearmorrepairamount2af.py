# shipBonusRemoteArmorRepairAmount2AF
#
# Used by:
# Ship: Inquisitor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
