# Not used by any item
type = "passive"
runTime = "early"


def handler(fit, module, context):
    fit.ship.preAssignItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadius"))
