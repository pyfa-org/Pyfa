# systemScanDurationSkillAstrometrics
#
# Used by:
# Implants named like: Poteque 'Prospector' Astrometric Acquisition AQ (3 of 3)
# Skill: Astrometric Acquisition
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                  "duration", container.getModifiedItemAttr("durationBonus") * level)
