# Used by:
# Variations of module: 100MN Afterburner I (24 of 24)
# Variations of module: 10MN Afterburner I (14 of 14)
# Variations of module: 1MN Afterburner I (15 of 15)
# Module: Civilian Afterburner
type = "active"
runTime = "late"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
    speedBoost = module.getModifiedItemAttr("speedFactor")
    mass = fit.ship.getModifiedItemAttr("mass")
    thrust = module.getModifiedItemAttr("speedBoostFactor")
    fit.ship.boostItemAttr("maxVelocity", speedBoost * thrust / mass)
