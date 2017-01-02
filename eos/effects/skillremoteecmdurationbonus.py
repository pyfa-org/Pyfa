# skillRemoteECMDurationBonus
#
# Used by:
# Skill: Burst Projector Operation
type = "passive"


def handler(fit, skill, context):
    # We need to make sure that the attribute exists, otherwise we add attributes that don't belong.  See #927
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                              mod.item.getAttribute("duration"),
                                  "duration",
                                  skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                              mod.item.getAttribute("durationECMJammerBurstProjector"),
                                  "durationECMJammerBurstProjector",
                                  skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                              mod.item.getAttribute("durationTargetIlluminationBurstProjector"),
                                  "durationTargetIlluminationBurstProjector",
                                  skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                              mod.item.getAttribute("durationSensorDampeningBurstProjector"),
                                  "durationSensorDampeningBurstProjector",
                                  skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation") and
                                              mod.item.getAttribute("durationWeaponDisruptionBurstProjector"),
                                  "durationWeaponDisruptionBurstProjector",
                                  skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
