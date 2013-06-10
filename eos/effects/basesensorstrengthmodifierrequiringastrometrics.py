# Used by:
# Modules from group: Scan Probe Launcher (4 of 7)
# Implants named like: Low grade Virtue (5 of 6)
# Implants named like: Poteque 'Prospector' Astrometric Rangefinding AR (3 of 3)
# Modules named like: Gravity Capacitor Upgrade (8 of 8)
# Skill: Astrometric Rangefinding
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", container.getModifiedItemAttr("scanStrengthBonus") * level)
