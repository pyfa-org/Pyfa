# subsystemBonusAmarrOffensive2EnergyWeaponCapacitorNeed
#
# Used by:
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", module.getModifiedItemAttr("subsystemBonusAmarrOffensive2"),
                                  skill="Amarr Offensive Systems")
