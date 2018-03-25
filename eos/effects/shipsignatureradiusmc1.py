# shipSignatureRadiusMC1
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("signatureRadius", src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
