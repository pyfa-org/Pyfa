# subsystemBonusCaldariDefensiveShieldHP
#
# Used by:
# Subsystem: Tengu Defensive - Supplemental Screening
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("subsystemBonusCaldariDefensive"), skill="Caldari Defensive Systems")
