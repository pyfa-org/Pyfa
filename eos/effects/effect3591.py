# ewSkillSignalSuppressionMaxTargetRangeBonus
#
# Used by:
# Modules named like: Inverted Signal Field Projector (8 of 8)
# Skill: Signal Suppression
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                  "maxTargetRangeBonus",
                                  container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)
