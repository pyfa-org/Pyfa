# Used by:
# Subsystem: Tengu Propulsion - Intercalated Nanofibers
# Subsystem: Tengu Propulsion - Interdiction Nullifier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Propulsion Systems").level
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion") * level)
