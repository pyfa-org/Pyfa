type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Micro Jump Drive Operation"), "duration", src.getModifiedItemAttr("eliteBonusCommandDestroyer2"), skill="Command Destroyers")
