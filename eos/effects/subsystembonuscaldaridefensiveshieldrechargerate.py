# subsystemBonusCaldariDefensiveShieldRechargeRate
#
# Used by:
# Subsystem: Tengu Defensive - Supplemental Screening
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Defensive Systems").level
    fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariDefensive2") * level)
