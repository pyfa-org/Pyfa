# Used by:
# Skill: Signature Focusing
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", skill.getModifiedItemAttr("scanSkillTargetPaintStrengthBonus") * skill.level)