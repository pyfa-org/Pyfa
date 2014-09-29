# shipMissileExploDamageCB
#
# Used by:
# Ship: Barghest
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusCB") * level)
