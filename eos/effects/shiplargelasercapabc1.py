# Used by:
# Ship: Oracle
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC1") * level)
