# modeAgilityPostDiv
#
# Used by:
# Modules named like: Propulsion Mode (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("agility", 1/module.getModifiedItemAttr("modeAgilityPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
