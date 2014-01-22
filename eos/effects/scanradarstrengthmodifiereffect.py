# Used by:
# Implant: Low-grade Grail Alpha
# Implant: Low-grade Grail Beta
# Implant: Low-grade Grail Delta
# Implant: Low-grade Grail Epsilon
# Implant: Low-grade Grail Gamma
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanRadarStrength", implant.getModifiedItemAttr("scanRadarStrengthModifier"))