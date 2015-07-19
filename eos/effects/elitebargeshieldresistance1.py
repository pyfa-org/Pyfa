# eliteBargeShieldResistance1
#
# Used by:
# Ships from group: Exhumer (3 of 3)
type = "passive"
def handler(fit, ship, context):
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusBarge1"), skill="Exhumers")
