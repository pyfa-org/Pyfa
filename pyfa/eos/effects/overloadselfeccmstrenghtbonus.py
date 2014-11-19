# overloadSelfECCMStrenghtBonus
#
# Used by:
# Modules from group: ECCM (44 of 44)
# Modules from group: Projected ECCM (7 of 7)
type = "overheat"
def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        module.boostItemAttr("scan%sStrengthPercent" % scanType,
                             module.getModifiedItemAttr("overloadECCMStrenghtBonus"))
