# Not used by any item
runTime = "early"
type = "passive"


def handler(fit, module, context):
    fit.ship.preAssignItemAttr("agility", module.getModifiedItemAttr("agility"))
