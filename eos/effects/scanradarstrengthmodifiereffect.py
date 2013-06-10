# Used by:
# Implants named like: Low grade Grail (5 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.ship.increaseItemAttr("scanRadarStrength", implant.getModifiedItemAttr("scanRadarStrengthModifier"))