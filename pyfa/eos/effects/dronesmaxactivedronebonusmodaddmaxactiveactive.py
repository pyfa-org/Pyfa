# dronesMaxActiveDroneBonusModAddMaxActiveActive
#
# Used by:
# Modules from group: Drone Control Unit (5 of 5)
type = "active"
def handler(fit, module, context):
    amount = module.getModifiedItemAttr("maxActiveDroneBonus")
    fit.extraAttributes.increase("maxActiveDrones", amount)
