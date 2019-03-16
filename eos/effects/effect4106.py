# subsystemBonusGallenteOffensiveHybridWeaponFalloff
#
# Used by:
# Subsystem: Proteus Offensive - Hybrid Encoding Platform
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", module.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                  skill="Gallente Offensive Systems")
