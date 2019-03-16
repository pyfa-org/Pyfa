# armorReinforcerMassAdd
#
# Used by:
# Modules from group: Armor Reinforcer (51 of 51)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
