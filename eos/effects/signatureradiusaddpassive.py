type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadius"))
