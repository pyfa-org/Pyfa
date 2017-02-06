# shipBonusShieldExplosiveResistanceCD2
#
# Used by:
# Ship: Stork
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusCD2"),
                           skill="Caldari Destroyer")
