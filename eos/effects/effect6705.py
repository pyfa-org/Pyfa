# rigDrawbackReductionShield
#
# Used by:
# Skill: Shield Rigging
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Shield", "drawback",
                                  src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
