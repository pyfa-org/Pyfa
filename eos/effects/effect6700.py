# rigDrawbackReductionElectronic
#
# Used by:
# Skill: Electronic Superiority Rigging
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Electronic Systems", "drawback",
                                  src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Scanning", "drawback",
                                  src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Targeting", "drawback",
                                  src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
