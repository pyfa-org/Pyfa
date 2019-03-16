# subsystemBonusGallenteCore3WarpScramHeatBonus
#
# Used by:
# Subsystem: Proteus Core - Friction Extension Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "overloadRangeBonus",
                                  src.getModifiedItemAttr("subsystemBonusGallenteCore3"), skill="Gallente Core Systems")
