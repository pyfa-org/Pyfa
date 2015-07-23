# shipHeavyAssaultMissileVelocityCBC2
#
# Used by:
# Ship: Drake Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")
