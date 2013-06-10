# Used by:
# Skill: EM Shield Compensation
type = "passive"
def handler(fit, skill, context):
    level = fit.character.getSkill("EM Shield Compensation").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Amplifier",
                                  "emDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * level)