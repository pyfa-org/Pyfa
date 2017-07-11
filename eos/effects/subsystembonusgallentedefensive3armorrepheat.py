# subsystemBonusGallenteDefensive3ArmorRepHeat
#
# Used by:
# Subsystem: Proteus Defensive - Covert Reconfiguration
# Subsystem: Proteus Defensive - Nanobot Injector
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"),
                                  skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"),
                                  skill="Gallente Defensive Systems")
