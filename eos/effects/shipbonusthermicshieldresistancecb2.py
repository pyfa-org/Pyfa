# shipBonusThermicShieldResistanceCB2
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
# Ship: Rokh
# Ship: Scorpion Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                           skill="Caldari Battleship")
