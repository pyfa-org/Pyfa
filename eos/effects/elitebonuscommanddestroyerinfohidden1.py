# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"),
                                  "commandBonusHidden",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer1"),
                                  skill="Command Destroyers")
