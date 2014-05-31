type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Expedition Frigates").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", module.getModifiedItemAttr("eliteBonusExpedition1") * level)
