# skillReactiveArmorHardenerDurationBonus
#
# Used by:
# Skill: Resistance Phasing
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Resistance Shift Hardener",
                                  "duration", skill.getModifiedItemAttr("durationBonus") * skill.level)
