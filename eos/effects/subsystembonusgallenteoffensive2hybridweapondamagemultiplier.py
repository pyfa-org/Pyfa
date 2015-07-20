# subsystemBonusGallenteOffensive2HybridWeaponDamageMultiplier
#
# Used by:
# Variations of subsystem: Proteus Offensive - Dissonic Encoding Platform (3 of 4)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive2"), skill="Gallente Offensive Systems")
