# speedBoostMassSigRad
#
# Used by:
# Variations of module: 500MN Microwarpdrive I (26 of 26)
# Variations of module: 50MN Microwarpdrive I (16 of 16)
# Variations of module: 5MN Microwarpdrive I (16 of 16)
type = "active"
runTime = "late"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
    speedBoost = module.getModifiedItemAttr("speedFactor")
    mass = fit.ship.getModifiedItemAttr("mass")
    thrust = module.getModifiedItemAttr("speedBoostFactor")
    fit.ship.boostItemAttr("maxVelocity", speedBoost * thrust / mass)
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"), stackingPenalties = True)
