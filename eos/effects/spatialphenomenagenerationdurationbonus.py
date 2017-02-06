# spatialPhenomenaGenerationDurationBonus
#
# Used by:
# Skill: Spatial Phenomena Generation
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Spatial Phenomena Generation"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
