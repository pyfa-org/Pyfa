type = "active"

def handler(fit, module, context):
    for x in xrange(1, 4):
        value = module.getModifiedChargeAttr("warfareBuff{}Multiplier".format(x))
        module.multiplyItemAttr("warfareBuff{}Value".format(x), value)