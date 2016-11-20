# overloadSelfECMStrenghtBonus
#
# Used by:
# Modules from group: Burst Jammer (11 of 11)
# Modules from group: ECM (39 of 39)
type = "overheat"


def handler(fit, module, context):
    if "projected" not in context:
        for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            module.boostItemAttr("scan{0}StrengthBonus".format(scanType),
                                 module.getModifiedItemAttr("overloadECMStrengthBonus"),
                                 stackingPenalties=True)
