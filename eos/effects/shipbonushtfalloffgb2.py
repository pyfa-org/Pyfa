# shipBonusHTFalloffGB2
#
# Used by:
# Ship: Kronos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGB2") * level)
