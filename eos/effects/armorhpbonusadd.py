# armorHPBonusAdd
#
# Used by:
# Modules from group: Armor Reinforcer (48 of 48)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("armorHP", module.getModifiedItemAttr("armorHPBonusAdd"))
