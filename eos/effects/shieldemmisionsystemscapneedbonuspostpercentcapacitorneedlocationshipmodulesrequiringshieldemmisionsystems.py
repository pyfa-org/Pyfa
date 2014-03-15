# Used by:
# Implants named like: Zainou 'Gnome' Shield Emission Systems SE (6 of 6)
# Skill: Shield Emission Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
