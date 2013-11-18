# Used by:
# Ship: Flycatcher
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCD2") * level)
