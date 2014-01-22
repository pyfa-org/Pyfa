# Used by:
# Implants named like: Inherent Implants Emission Systems ES (6 of 6)
# Modules named like: Egress (8 of 8)
# Skill: Capacitor Emission Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
