# Used by:
# Implants named like: Halo (10 of 12)
# Implants named like: X Instinct Booster (4 of 4)
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("signatureRadius", implant.getModifiedItemAttr("signatureRadiusBonus"))
