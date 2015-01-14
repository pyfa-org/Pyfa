# shipBonusHeavyDroneArmorHpPirateFaction
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
# Ship: 响尾蛇级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusPirateFaction"))
