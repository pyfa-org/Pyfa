# Used by:
# Implants named like: Low grade Jackal (5 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanLadarStrength", implant.getModifiedItemAttr("scanLadarStrengthModifier"))