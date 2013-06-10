# Used by:
# Implants named like: Low grade Talon (5 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanGravimetricStrength", implant.getModifiedItemAttr("scanGravimetricStrengthModifier"))