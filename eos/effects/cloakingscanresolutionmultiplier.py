# Used by:
# Modules from group: Cloaking Device (12 of 14)
type = "offline"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanResolution",
                              module.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties = True, penaltyGroup="cloakingScanResolutionMultiplier")
