# eliteBonusCommandShipsHeavyMissileExplosionRadiusCS2
#
# Used by:
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("eliteBonusCommandShips2") * level)
