# Used by:
# Ship: Venture
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Mining Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", module.getModifiedItemAttr("shipBonusOREfrig1") * level)