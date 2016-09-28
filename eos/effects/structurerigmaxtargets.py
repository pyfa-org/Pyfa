# Not used by any item
type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("structureRigMaxTargetBonus"))
