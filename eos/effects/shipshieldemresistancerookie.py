# shipShieldEMResistanceRookie
#
# Used by:
# Ship: Ibis
# Ship: Taipan
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))
