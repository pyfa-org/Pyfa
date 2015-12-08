type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange", src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
