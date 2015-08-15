# shipMissileKineticDamageCC
#
# Used by:
# Ship: Cerberus
# Ship: Onyx
# Ship: Orthrus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
