# signatureAnalysisScanResolutionBonusPostPercentScanResolutionShip
#
# Used by:
# Implants named like: Zainou 'Gypsy' Signature Analysis SA (6 of 6)
# Modules named like: Targeting System Subcontroller (8 of 8)
# Implant: Quafe Zero
# Skill: Signature Analysis
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    penalized = False if "skill" in context or "implant" in context or "booster" in context else True
    fit.ship.boostItemAttr("scanResolution", container.getModifiedItemAttr("scanResolutionBonus") * level,
                           stackingPenalties=penalized)
