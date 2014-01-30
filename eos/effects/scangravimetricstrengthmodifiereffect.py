# Used by:
# Implant: Low-grade Talon Alpha
# Implant: Low-grade Talon Beta
# Implant: Low-grade Talon Delta
# Implant: Low-grade Talon Epsilon
# Implant: Low-grade Talon Gamma
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanGravimetricStrength", implant.getModifiedItemAttr("scanGravimetricStrengthModifier"))