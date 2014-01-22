# Used by:
# Implant: Poteque 'Prospector' Astrometric Pinpointing AP-602
# Implant: Poteque 'Prospector' Astrometric Pinpointing AP-606
# Implant: Poteque 'Prospector' Astrometric Pinpointing AP-610
# Skill: Astrometric Pinpointing
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseMaxScanDeviation", container.getModifiedItemAttr("maxScanDeviationModifier") * level)
