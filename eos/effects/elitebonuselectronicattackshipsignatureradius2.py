# eliteBonusElectronicAttackShipSignatureRadius2
#
# Used by:
# Ship: Hyena
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"), skill="Electronic Attack Ships")
