# overloadSelfECMStrenghtBonus
#
# Used by:
# Modules from group: ECM (44 of 44)
# Modules from group: ECM Burst (7 of 7)
type = "overheat"
def handler(fit, module, context):
    if "projected" not in context:
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            module.boostItemAttr("scan{0}StrengthBonus".format(scanType),
                                 module.getModifiedItemAttr("overloadECMStrengthBonus"),
                                 stackingPenalties = True)
