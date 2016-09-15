type = "passive"
def handler(fit, src, context):
    fit.ship.filteredItemIncrease("maxLockedTargets", src.getModifiedItemAttr("structureRigMaxTargetBonus"))
