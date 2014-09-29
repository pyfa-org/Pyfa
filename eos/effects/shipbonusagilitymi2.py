# shipBonusAgilityMI2
#
# Used by:
# Ship: Wreathe
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Industrial").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusMI2") * level)
