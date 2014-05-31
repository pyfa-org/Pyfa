# Used by:
# Modules from group: Scan Probe Launcher (4 of 7)
# Implants named like: Low grade Virtue (10 of 12)
# Implants named like: Poteque 'Prospector' Astrometric Rangefinding AR (3 of 3)
# Modules named like: Gravity Capacitor Upgrade (8 of 8)
# Skill: Astrometric Rangefinding
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    penalized = False if "skill" in context or "implant" in context else True
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", container.getModifiedItemAttr("scanStrengthBonus") * level,
                                    stackingPenalties=penalized)
