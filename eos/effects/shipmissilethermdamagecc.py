# shipMissileThermDamageCC
#
# Used by:
# Ship: Orthrus
# Ship: Osprey Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
