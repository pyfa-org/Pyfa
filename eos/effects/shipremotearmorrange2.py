# shipRemoteArmorRange2
#
# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
