# shipBonusExplosiveShieldResistanceCB2
#
# Used by:
# Ship: Rattlesnake
# Ship: Rokh
# Ship: Scorpion Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                           skill="Caldari Battleship")
