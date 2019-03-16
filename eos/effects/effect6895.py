# subsystemMETFittingReduction
#
# Used by:
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "cpu", src.getModifiedItemAttr("subsystemMETFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "power", src.getModifiedItemAttr("subsystemMETFittingReduction"))
