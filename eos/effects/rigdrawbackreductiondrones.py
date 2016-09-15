# rigDrawbackReductionDrones
#
# Used by:
# Skill: Drones Rigging
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Drones", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
