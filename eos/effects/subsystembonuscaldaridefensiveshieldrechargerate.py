# subsystemBonusCaldariDefensiveShieldRechargeRate
#
# Used by:
# Subsystem: Tengu Defensive - Supplemental Screening
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariDefensive2"), skill="Caldari Defensive Systems")
