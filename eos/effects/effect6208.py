# microJumpPortalDrive
#
# Used by:
# Module: Micro Jump Field Generator
type = "active"


def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonusPercent"),
                           stackingPenalties=True)
