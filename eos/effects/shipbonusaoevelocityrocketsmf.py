# shipBonusAoeVelocityRocketsMF
#
# Used by:
# Ship: Vigil Fleet Issue
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "aoeVelocity",
                                    src.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
