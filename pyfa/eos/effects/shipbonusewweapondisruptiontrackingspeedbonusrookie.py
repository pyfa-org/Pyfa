# shipBonusEwWeaponDisruptionTrackingSpeedBonusRookie
#
# Used by:
# Ship: Impairor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("rookieWeaponDisruptionBonus"))
