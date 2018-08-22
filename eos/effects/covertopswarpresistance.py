type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpFactor", src.getModifiedItemAttr("eliteBonusCovertOps1"), skill="Covert Ops")
