# structureStealthEmitterArraySigDecrease
#
# Used by:
# Implants named like: X Instinct Booster (4 of 4)
# Implants named like: grade Halo (15 of 18)
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("signatureRadius", implant.getModifiedItemAttr("signatureRadiusBonus"))
