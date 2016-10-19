# shipBonusTitanM4FleetBonus
#
# Used by:
# Ship: Ragnarok
type = "gang"
gangBoost = "signatureRadius"
gangBonus = "shipBonusTitanM4"
gangBonusSkill = "Minmatar Titan"
runTime = "late"


def handler(fit, src, context):
    if "gang" not in context: return
    fit.ship.boostItemAttr(gangBoost,
                           src.getModifiedItemAttr(gangBonus) * src.parent.character.getSkill(gangBonusSkill).level)
