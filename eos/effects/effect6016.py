# modeAgilityPostDiv
#
# Used by:
# Modules named like: Propulsion Mode (4 of 4)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "agility",
        1 / module.getModifiedItemAttr("modeAgilityPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
