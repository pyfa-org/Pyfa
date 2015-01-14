# shipMissileKinDamageCC2
#
# Used by:
# Ship: Osprey Navy Issue
# Ship: Rook
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCC2") * level)
