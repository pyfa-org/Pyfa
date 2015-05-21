# modeAgilityPostDiv
#
# Used by:
# Modules named like: Propulsion Mode (3 of 3)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "agility",
        1 / module.getModifiedItemAttr("modeAgilityPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
