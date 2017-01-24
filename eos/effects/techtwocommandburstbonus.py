# Not used by any item
type = "passive"
runTime = "late"


def handler(fit, module, context):
    for x in xrange(1, 4):
        module.boostChargeAttr("warfareBuff{}Multiplier".format(x), module.getModifiedItemAttr("commandBurstStrengthBonus"))
