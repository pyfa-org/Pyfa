# shipLargeHybridTurretRofGB
#
# Used by:
# Ships named like: Megathron (5 of 6)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusGB") * level)
