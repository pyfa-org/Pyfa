# surveyScanspeedBonusPostPercentDurationLocationShipModulesRequiringElectronics
#
# Used by:
# Modules named like: Signal Focusing Kit (8 of 8)
# Skill: Survey
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("CPU Management"),
                                  "duration", container.getModifiedItemAttr("scanspeedBonus") * level)
