type = "passive"
runTime = "late"

def handler(fit, module, context):
    for x in xrange(1, 4):
        module.boostChargeAttr("warfareBuff{}Value".format(x), module.getModifiedItemAttr("commandBurstStrengthBonus"))
