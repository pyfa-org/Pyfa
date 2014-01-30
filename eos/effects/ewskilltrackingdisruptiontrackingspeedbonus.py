# Used by:
# Modules named like: Tracking Diagnostic (8 of 8)
# Skill: Turret Destabilization
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "trackingSpeedBonus", container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)
