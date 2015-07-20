# subsystemBonusCaldariOffensiveHybridWeaponMaxRange
#
# Used by:
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
