# Used by:
# Modules named like: Core Operational Solidifier (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "duration", module.getModifiedItemAttr("durationSkillBonus"))