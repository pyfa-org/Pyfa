# Used by:
# Implants named like: Inherent Implants 'Lancer' Controlled Bursts CB (6 of 6)
# Skill: Controlled Bursts
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
