# overloadSelfHardeningInvulnerabilityBonus
#
# Used by:
# Modules named like: Capital Flex Hardener (9 of 9)
# Variations of module: Adaptive Invulnerability Field I (17 of 17)
type = "overheat"


def handler(fit, module, context):
    for type in ("kinetic", "thermal", "explosive", "em"):
        module.boostItemAttr("%sDamageResistanceBonus" % type,
                             module.getModifiedItemAttr("overloadHardeningBonus"))