# Used by:
# Implants named like: Inherent Implants 'Lancer' Gunnery RF (6 of 6)
# Implant: Pashan's Turret Customization Mindlink
# Skill: Gunnery
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "speed", container.getModifiedItemAttr("turretSpeeBonus") * level)
