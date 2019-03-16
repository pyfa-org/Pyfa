# shipMissileKinDamageCC2
#
# Used by:
# Ship: Rook
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
