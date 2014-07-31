# Used by:
# Subsystem: Proteus Propulsion - Interdiction Nullifier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Propulsion Systems").level
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusGallentePropulsion") * level)
