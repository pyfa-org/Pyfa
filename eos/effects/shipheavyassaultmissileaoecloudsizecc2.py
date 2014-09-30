# shipHeavyAssaultMissileAOECloudSizeCC2
#
# Used by:
# Ship: Caracal Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCC2") * level)
