# Used by:
# Modules from group: ECM (44 of 44)
type = "overheat"
def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        module.boostItemAttr("scan{0}StrengthBonus".format(scanType),
                             module.getModifiedItemAttr("overloadECMStrengthBonus"),
                             stackingPenalties = True)
