type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCF2") * level)
