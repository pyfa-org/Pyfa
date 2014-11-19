# shieldOperationRechargeratebonusPostPercentOnline
#
# Used by:
# Modules from group: Shield Power Relay (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("rechargeratebonus") or 0)
