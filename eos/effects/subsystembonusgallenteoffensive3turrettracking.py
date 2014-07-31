# Used by:
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", module.getModifiedItemAttr("subsystemBonusGallenteOffensive3") * level)
