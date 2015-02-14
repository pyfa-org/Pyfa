# shipModeScanStrengthPostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanRadarStrength", 1/module.getModifiedItemAttr("modeRadarStrengthPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
