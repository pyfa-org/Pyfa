# eliteBonusBlackOpsECMGravAndLadarAndMagnetometricAndRadarStrength1
#
# Used by:
# Ship: Widow
type = "passive"
def handler(fit, ship, context):
    sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
    for type in sensorTypes:
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scan{0}StrengthBonus".format(type),
                                      ship.getModifiedItemAttr("eliteBonusBlackOps1"), skill="Black Ops")
