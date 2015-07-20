# eliteBonusExpeditionSigRadius2
#
# Used by:
# Ship: Prospect
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusExpedition2"), skill="Expedition Frigates")
