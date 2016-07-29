# rigDrawbackReductionEnergyWeapon
#
# Used by:
# Skill: Energy Weapon Rigging
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Energy Weapon", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
