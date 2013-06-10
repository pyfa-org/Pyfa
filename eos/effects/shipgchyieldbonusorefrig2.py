# Used by:
# Ship: Venture
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Mining Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gas Cloud Harvesting"),
                                     "duration", module.getModifiedItemAttr("shipBonusOREfrig2") * level)