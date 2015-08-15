# shipBonusMissileVelocityCC2
#
# Used by:
# Ship: Cerberus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
