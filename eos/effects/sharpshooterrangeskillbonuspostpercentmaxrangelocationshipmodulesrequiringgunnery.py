# Used by:
# Implants named like: ST (6 of 6)
# Implant: Improved Frentix Booster
# Implant: Standard Frentix Booster
# Implant: Strong Frentix Booster
# Implant: Synth Frentix Booster
# Skill: Sharpshooter
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level)
