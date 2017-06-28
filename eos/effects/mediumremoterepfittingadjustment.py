type = "passive"


def handler(fit, module, context):
    module.multiply("power", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))
    module.multiply("cpu", module.getModifiedItemAttr("mediumRemoteRepFittingMultiplier"))
