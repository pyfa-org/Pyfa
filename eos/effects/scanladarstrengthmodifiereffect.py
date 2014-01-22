# Used by:
# Implant: Low-grade Jackal Alpha
# Implant: Low-grade Jackal Beta
# Implant: Low-grade Jackal Delta
# Implant: Low-grade Jackal Epsilon
# Implant: Low-grade Jackal Gamma
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanLadarStrength", implant.getModifiedItemAttr("scanLadarStrengthModifier"))