# heatDamageBonus
#
# Used by:
# Modules from group: Shield Boost Amplifier (25 of 25)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "heatDamage", module.getModifiedItemAttr("heatDamageBonus"))
