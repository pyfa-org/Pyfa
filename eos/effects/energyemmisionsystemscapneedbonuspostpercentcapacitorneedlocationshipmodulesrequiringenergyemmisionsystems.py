# Used by:
# Implants named like: Inherent Implants 'Squire' Energy Emission Systems ES (6 of 6)
# Modules named like: Egress Port Maximizer (8 of 8)
# Skill: Energy Emission Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Emission Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
