# shipShieldExplosiveResistanceRookie
#
# Used by:
# Ship: Broadsword
# Ship: Ibis
# Ship: Onyx
# Ship: Taipan
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))
