# Used by:
# Modules named like: Nanobot Accelerator (8 of 8)
# Skill: Capital Repair Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "duration", container.getModifiedItemAttr("durationSkillBonus") * level,
                                  stackingPenalties = "skill" not in context)
