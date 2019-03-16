# subsystemBonusAmarrOffensive3EnergyWeaponMaxRange
#
# Used by:
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusAmarrOffensive3"),
                                  skill="Amarr Offensive Systems")
