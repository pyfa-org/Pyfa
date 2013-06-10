# Used by:
# Ship: Megathron
# Ship: Megathron Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusGB") * level)
