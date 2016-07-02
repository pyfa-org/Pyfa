type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Rig Launcher", "drawback", src.getModifiedItemAttr("rigDrawbackBonus") * lvl)
