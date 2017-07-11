# subsystemBonusGallenteOffensive2HybridWeaponDamageMultiplier
#
# Used by:
# Subsystem: Proteus Offensive - Hybrid Encoding Platform
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                  skill="Gallente Offensive Systems")
