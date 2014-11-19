# shipMissileAssaultMissileVelocityBonusCC2
#
# Used by:
# Ships named like: Caracal (3 of 4)
# Ship: Osprey Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2") * level)
