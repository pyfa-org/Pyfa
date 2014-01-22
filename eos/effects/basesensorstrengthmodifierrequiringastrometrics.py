# Used by:
# Modules named like: Gravity Capacitor Upgrade (8 of 8)
# Implant: Low-grade Virtue Alpha
# Implant: Low-grade Virtue Beta
# Implant: Low-grade Virtue Delta
# Implant: Low-grade Virtue Epsilon
# Implant: Low-grade Virtue Gamma
# Implant: Poteque 'Prospector' Astrometric Rangefinding AR-802
# Implant: Poteque 'Prospector' Astrometric Rangefinding AR-806
# Implant: Poteque 'Prospector' Astrometric Rangefinding AR-810
# Module: Core Probe Launcher II
# Module: Expanded Probe Launcher II
# Module: Sisters Core Probe Launcher
# Module: Sisters Expanded Probe Launcher
# Skill: Astrometric Rangefinding
# Skill: Astrometrics
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    penalized = False if "skill" in context or "implant" in context else True
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", container.getModifiedItemAttr("scanStrengthBonus") * level,
                                    stackingPenalties=penalized)
