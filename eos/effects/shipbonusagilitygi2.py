# Used by:
# Ship: Nereus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusGI2") * level)
