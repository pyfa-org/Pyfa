# eliteBonusLogiFrigSignature2
#
# Used by:
# Ship: Scalpel
# Ship: Thalia
type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("signatureRadius", src.getModifiedItemAttr("eliteBonusLogiFrig2"), skill="Logistics Frigates")
