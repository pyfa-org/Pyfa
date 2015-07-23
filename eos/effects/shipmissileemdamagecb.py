# shipMissileEMDamageCB
#
# Used by:
# Ship: Barghest
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "emDamage", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
