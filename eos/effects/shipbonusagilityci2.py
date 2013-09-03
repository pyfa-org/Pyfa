# Used by:
# Ship: Badger
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Industrial").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusCI2") * level)
