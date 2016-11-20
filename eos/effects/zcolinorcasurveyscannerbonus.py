type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Survey Scanner", "surveyScanRange", src.getModifiedItemAttr("roleBonusSurveyScannerRange"))
