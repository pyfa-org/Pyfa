type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange", src.getModifiedItemAttr("roleBonus"))
