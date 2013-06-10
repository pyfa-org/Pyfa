# Used by:
# Ship: Kitsune
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Electronic Attack Ships").level
    fit.ship.boostItemAttr("capacitorCapacity", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2") * level)
