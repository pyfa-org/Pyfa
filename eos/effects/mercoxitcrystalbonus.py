# mercoxitCrystalBonus
#
# Used by:
# Module: Medium Mercoxit Mining Crystal Optimization I
type = "passive"
runTime = "early"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Mercoxit Processing"),
                                    "specialisationAsteroidYieldMultiplier",
                                    module.getModifiedItemAttr("miningAmountBonus"))
