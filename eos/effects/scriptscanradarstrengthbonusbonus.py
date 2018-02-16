# scriptscanRadarStrengthBonusBonus
#
# Used by:
# Charges from group: Structure ECM script (4 of 4)
type = "passive"
runTime = "early"


def handler(fit, src, context, *args, **kwargs):
    src.boostItemAttr("scanRadarStrengthBonus", src.getModifiedChargeAttr("scanRadarStrengthBonusBonus"))
