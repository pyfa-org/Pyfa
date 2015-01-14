# shipBonusHeavyDRoneTrackingGC
#
# Used by:
# Ship: Ishtar
# Ship: 伊什塔级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC") * level)
