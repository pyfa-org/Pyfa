# armorReinforcerMassAdd
#
# Used by:
# Modules from group: Armor Reinforcer (57 of 57)
# Modules from group: Entosis Link (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))