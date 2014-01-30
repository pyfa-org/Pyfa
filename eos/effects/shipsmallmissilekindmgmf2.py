# Used by:
# Ship: Breacher
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusMF2") * level)
