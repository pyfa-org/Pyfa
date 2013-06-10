# Used by:
# Ship: Impairor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "maxRangeBonus", ship.getModifiedItemAttr("rookieWeaponDisruptionBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "falloffBonus", ship.getModifiedItemAttr("rookieWeaponDisruptionBonus"))
