# shipHTTrackingBonusGB2
#
# Used by:
# Ships named like: Megathron (6 of 6)
# Ship: 万王宝座级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB2") * level)
