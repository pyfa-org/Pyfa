# Used by:
# Subsystem: Proteus Propulsion - Gravitational Capacitor
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Propulsion Systems").level
    fit.ship.boostItemAttr("warpCapacitorNeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion2") * level)
