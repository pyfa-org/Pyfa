# Used by:
# Ship: Ragnarok
type = "gang"
gangBoost = "signatureRadius"
gangBonus = "titanMinmatarBonus2"
def handler(fit, ship, context):
    fit.ship.boostItemAttr(gangBoost, ship.getModifiedItemAttr(gangBonus))
