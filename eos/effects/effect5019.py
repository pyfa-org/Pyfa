# minmatarShipEwTargetPainterRookie
#
# Used by:
# Ship: Reaper
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("rookieTargetPainterStrengthBonus"))
