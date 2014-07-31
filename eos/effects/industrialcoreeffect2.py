# Used by:
# Module: Industrial Core I
type = "active"
runTime = "early"
def handler(fit, module, context):
    fit.extraAttributes["siege"] = True
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"))
    fit.ship.multiplyItemAttr("mass", module.getModifiedItemAttr("massMultiplier"))
