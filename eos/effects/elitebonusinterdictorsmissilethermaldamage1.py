# Used by:
# Ship: Eris
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interdictors").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"),
                                    "thermalDamage", ship.getModifiedItemAttr("eliteBonusInterdictors1") * level)
