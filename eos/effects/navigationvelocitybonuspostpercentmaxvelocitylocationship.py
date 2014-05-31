# Used by:
# Implants named like: Low grade Snake Alpha (2 of 2)
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("maxVelocity", implant.getModifiedItemAttr("velocityBonus"))