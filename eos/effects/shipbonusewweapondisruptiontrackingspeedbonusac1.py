# shipBonusEwWeaponDisruptionTrackingSpeedBonusAC1
#
# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
