# dreadnoughtShipBonusShieldResistancesC2
#
# Used by:
# Ships named like: Phoenix (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Dreadnought").level
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("dreadnoughtShipBonusC2") * level)
