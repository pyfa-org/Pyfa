# shipMissileAssaultMissileVelocityBonusCC2
#
# Used by:
# Ship: Caracal
# Ship: Osprey Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
