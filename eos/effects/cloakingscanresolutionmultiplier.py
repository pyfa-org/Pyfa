# Used by:
# Modules named like: Modified Cloaking Device (5 of 5)
# Module: Caldari Navy Cloaking Device
# Module: Dread Guristas Cloaking Device
# Module: Improved 'Guise' Cloaking Device II
# Module: Improved Cloaking Device II
# Module: Prototype 'Poncho' Cloaking Device I
# Module: Prototype Cloaking Device I
# Module: Syndicate Cloaking Device
type = "offline"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanResolution",
                              module.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties = True, penaltyGroup="cloakingScanResolutionMultiplier")
