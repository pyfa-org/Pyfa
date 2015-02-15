# modeMWDSigRadiusPostDiv
#
# Used by:
# Module: Svipul Defense Mode
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
        lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
        "signatureRadiusBonus",
        1 / module.getModifiedItemAttr("modeMWDSigPenaltyPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
