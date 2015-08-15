# eliteBonusCommandShipsHeavyAssaultMissileExplosionRadiusCS2
#
# Used by:
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
