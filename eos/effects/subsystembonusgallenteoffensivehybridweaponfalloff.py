# subsystemBonusGallenteOffensiveHybridWeaponFalloff
#
# Used by:
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
# Subsystem: Proteus Offensive - Hybrid Propulsion Armature
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", module.getModifiedItemAttr("subsystemBonusGallenteOffensive"), skill="Gallente Offensive Systems")
