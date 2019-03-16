# shieldOperationRechargeratebonusPostPercentOnline
#
# Used by:
# Modules from group: Shield Power Relay (6 of 6)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("rechargeratebonus") or 0)
