# Used by:
# Ship: Anathema
# Ship: Vengeance
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusAF") * level)
