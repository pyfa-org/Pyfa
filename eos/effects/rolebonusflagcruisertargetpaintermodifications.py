# roleBonusFlagCruiserTargetPainterModifications
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter", "signatureRadiusBonus",
                                  src.getModifiedItemAttr("targetPainterStrengthModifierFlagCruisers"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter", "maxRange",
                                  src.getModifiedItemAttr("targetPainterRangeModifierFlagCruisers"))
