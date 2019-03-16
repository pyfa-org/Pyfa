# subsystemBonusCaldariOffensive2HybridWeaponDamageMultiplier
#
# Used by:
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                  skill="Caldari Offensive Systems")
