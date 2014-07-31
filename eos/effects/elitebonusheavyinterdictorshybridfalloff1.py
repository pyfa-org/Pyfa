# Used by:
# Ship: Phobos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1") * level)
