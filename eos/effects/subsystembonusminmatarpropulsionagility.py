# Used by:
# Subsystem: Loki Propulsion - Intercalated Nanofibers
# Subsystem: Loki Propulsion - Interdiction Nullifier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Propulsion Systems").level
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion") * level)
