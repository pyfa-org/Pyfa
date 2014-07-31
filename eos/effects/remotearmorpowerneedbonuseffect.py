# Used by:
# Ship: Guardian
# Ship: Oneiros
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "power", ship.getModifiedItemAttr("remoteArmorPowerNeedBonus"))
