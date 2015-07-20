# shipBonusSmallMissileExplosionRadiusCF2
#
# Used by:
# Ship: Crow
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
