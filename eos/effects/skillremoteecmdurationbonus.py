# skillRemoteECMDurationBonus
#
# Used by:
# Skill: Burst Projector Operation
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Projectors",
                                  "duration", skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
