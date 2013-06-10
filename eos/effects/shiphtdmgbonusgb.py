# Used by:
# Ship: Dominix Navy Issue
# Ship: Hyperion
# Ship: Kronos
# Ship: Megathron Federate Issue
# Ship: Sin
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB") * level)
