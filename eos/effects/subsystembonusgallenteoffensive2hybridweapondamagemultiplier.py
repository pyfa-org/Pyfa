# Used by:
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
# Subsystem: Proteus Offensive - Drone Synthesis Projector
# Subsystem: Proteus Offensive - Hybrid Propulsion Armature
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive2") * level)
