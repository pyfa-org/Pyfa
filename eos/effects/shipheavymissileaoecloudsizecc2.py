# shipHeavyMissileAOECloudSizeCC2
#
# Used by:
# Ship: Caracal Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
