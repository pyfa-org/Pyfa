# Used by:
# Modules named like: Core Defense Capacitor Safeguard (8 of 8)
# Skill: Shield Compensation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "capacitorNeed", container.getModifiedItemAttr("shieldBoostCapacitorBonus") * level)
