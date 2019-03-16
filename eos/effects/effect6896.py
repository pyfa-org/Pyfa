# subsystemMHTFittingReduction
#
# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
# Subsystem: Proteus Offensive - Hybrid Encoding Platform
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "cpu", src.getModifiedItemAttr("subsystemMHTFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "power", src.getModifiedItemAttr("subsystemMHTFittingReduction"))
