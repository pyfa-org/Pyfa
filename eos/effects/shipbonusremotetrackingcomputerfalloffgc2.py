# shipBonusRemoteTrackingComputerFalloffGC2
#
# Used by:
# Ship: Oneiros
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                  "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
