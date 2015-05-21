# armorHPBonusAdd
#
# Used by:
# Modules from group: Armor Reinforcer (38 of 38)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("armorHP", module.getModifiedItemAttr("armorHPBonusAdd"))