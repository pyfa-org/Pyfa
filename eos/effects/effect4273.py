# subsystemBonusGallenteCore2WarpScrambleRange
#
# Used by:
# Subsystem: Proteus Core - Friction Extension Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                  src.getModifiedItemAttr("subsystemBonusGallenteCore2"), skill="Gallente Core Systems")
