# dreadnoughtShipBonusShieldResistancesC2
#
# Used by:
# Ship: Phoenix
type = "passive"
def handler(fit, ship, context):
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("dreadnoughtShipBonusC2"), skill="Caldari Dreadnought")
