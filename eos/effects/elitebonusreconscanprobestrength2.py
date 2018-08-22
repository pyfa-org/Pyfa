# eliteBonusReconScanProbeStrength2
#
# Used by:
# Ship: Tiamat
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength",
                                    src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
