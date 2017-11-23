# agilityBonus
#
# Used by:
# Subsystems named like: Propulsion Interdiction Nullifier (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("agility", src.getModifiedItemAttr("agilityBonusAdd"))
