# speedBoostMassAddition
#
# Used by:
# Variations of module: 100MN Afterburner I (25 of 25)
# Variations of module: 10MN Afterburner I (15 of 15)
# Variations of module: 1MN Afterburner I (16 of 16)
type = "active"
runTime = "late"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
    speedBoost = module.getModifiedItemAttr("speedFactor")
    mass = fit.ship.getModifiedItemAttr("mass")
    thrust = module.getModifiedItemAttr("speedBoostFactor")
    fit.ship.boostItemAttr("maxVelocity", speedBoost * thrust / mass)
