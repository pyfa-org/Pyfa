# shipBonusMediumDroneArmorHPPirateFaction
#
# Used by:
# Ship: Chameleon
# Ship: Gila
# Ship: 毒蜥级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusPirateFaction"))
