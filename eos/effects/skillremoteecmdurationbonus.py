# skillRemoteECMDurationBonus
#
# Used by:
# Skill: Burst Projector Operation
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                  "durationECMJammerBurstProjector", skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
