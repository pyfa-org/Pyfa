# moduleBonusSkirmishWarfareLinkEvasiveManeuvers
#
# Used by:
# Variations of module: Skirmish Warfare Link - Evasive Maneuvers I (2 of 2)
type = "gang", "active"
gangBoost = "signatureRadius"
runTime = "late"

def handler(fit, module, context):
    if "gang" not in context: return
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("commandBonus"),
                           stackingPenalties = True)
