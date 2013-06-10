# Used by:
# Ship: Hyena
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Electronic Attack Ships").level
    fit.ship.boostItemAttr("signatureRadius", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2") * level)
