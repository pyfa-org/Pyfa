# Used by:
# Subsystem: Legion Propulsion - Interdiction Nullifier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Propulsion Systems").level
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion") * level)
