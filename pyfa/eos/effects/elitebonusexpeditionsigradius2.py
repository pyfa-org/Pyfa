# eliteBonusExpeditionSigRadius2
#
# Used by:
# Ship: Prospect
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Expedition Frigates").level
    fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusExpedition2") * level)
