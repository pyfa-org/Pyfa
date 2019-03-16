# armorHPBonusAddPassive
#
# Used by:
# Subsystems from group: Defensive Systems (9 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("armorHP", module.getModifiedItemAttr("armorHPBonusAdd") or 0)
