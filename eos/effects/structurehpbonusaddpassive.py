type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("hp", module.getModifiedItemAttr("structureHPBonusAdd") or 0)
