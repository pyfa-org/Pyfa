# armorReinforcerMassAdd
#
# Used by:
# Modules from group: Armor Reinforcer (41 of 41)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))