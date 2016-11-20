# shipBonusExplosiveShieldResistanceMD2
#
# Used by:
# Ship: Bifrost
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusMD2"),
                           skill="Minmatar Destroyer")
