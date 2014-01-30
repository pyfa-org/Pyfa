# Used by:
# Implant: Poteque 'Prospector' Astrometric Acquisition AQ-702
# Implant: Poteque 'Prospector' Astrometric Acquisition AQ-706
# Implant: Poteque 'Prospector' Astrometric Acquisition AQ-710
# Skill: Astrometric Acquisition
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                  "duration", container.getModifiedItemAttr("durationBonus") * level)
