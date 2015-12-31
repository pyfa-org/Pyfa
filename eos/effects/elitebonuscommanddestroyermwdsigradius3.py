# eliteBonusCommandDestroyerMWDSigRadius3
#
# Used by:
# Ships from group: Command Destroyers (4 of 4)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"), "signatureRadiusBonus", src.getModifiedItemAttr("eliteBonusCommandDestroyer3") * 5)  # * 5 because eliteBonusCommandDestroyer3 is only -10 when it should be -50
