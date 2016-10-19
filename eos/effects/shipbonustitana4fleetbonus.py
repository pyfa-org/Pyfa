# shipBonusTitanA4FleetBonus
#
# Used by:
# Ship: Avatar
type = "gang"
gangBoost = "rechargeRate"
gangBonus = "shipBonusTitanA4"
gangBonusSkill = "Amarr Titan"
runTime = "late"


def handler(fit, src, context):
    if "gang" not in context: return
    fit.ship.boostItemAttr(gangBoost,
                           src.getModifiedItemAttr(gangBonus) * src.parent.character.getSkill(gangBonusSkill).level)
