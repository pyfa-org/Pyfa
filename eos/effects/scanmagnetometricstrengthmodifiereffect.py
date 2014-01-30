# Used by:
# Implant: Low-grade Spur Alpha
# Implant: Low-grade Spur Beta
# Implant: Low-grade Spur Delta
# Implant: Low-grade Spur Epsilon
# Implant: Low-grade Spur Gamma
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanMagnetometricStrength", implant.getModifiedItemAttr("scanMagnetometricStrengthModifier"))