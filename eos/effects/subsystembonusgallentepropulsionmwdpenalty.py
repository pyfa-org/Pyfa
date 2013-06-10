# Used by:
# Subsystem: Proteus Propulsion - Wake Limiter
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Propulsion Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", module.getModifiedItemAttr("subsystemBonusGallentePropulsion") * level)
