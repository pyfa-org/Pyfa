type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Torpedo Specialization"), "speed", src.getModifiedItemAttr("rofBonus") * lvl)
