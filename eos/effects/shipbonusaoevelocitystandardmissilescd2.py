# Used by:
# Ship: Corax
# Ship: Flycatcher
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusCD2") * level)
