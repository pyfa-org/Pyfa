# structureModifyPowerRechargeRate
#
# Used by:
# Structure Modules from group: Structure Capacitor Power Relay (2 of 2)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("rechargeRate", module.getModifiedItemAttr("capacitorRechargeRateMultiplier"))
