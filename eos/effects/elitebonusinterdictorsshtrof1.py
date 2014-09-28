type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interdictors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("eliteBonusInterdictors1") * level)