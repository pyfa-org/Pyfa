# Used by:
# Skill: Armor Resistance Phasing
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Resistance Shift Hardener",
                                  "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)
