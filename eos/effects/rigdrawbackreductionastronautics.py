# rigDrawbackReductionAstronautics
#
# Used by:
# Skill: Astronautics Rigging
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Navigation", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Anchor", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
