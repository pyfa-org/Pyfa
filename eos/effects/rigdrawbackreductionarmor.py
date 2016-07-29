# rigDrawbackReductionArmor
#
# Used by:
# Skill: Armor Rigging
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Armor", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Resource Processing", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
