# Used by:
# Modules from group: ECCM (44 of 44)
type = "overheat"
def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        module.boostItemAttr("scan%sStrengthPercent" % scanType,
                             module.getModifiedItemAttr("overloadECCMStrenghtBonus"),
                             stackingPenalties = True)