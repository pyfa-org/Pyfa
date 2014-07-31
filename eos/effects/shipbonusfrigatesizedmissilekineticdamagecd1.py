# Used by:
# Ship: Corax
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCD1") * level)
