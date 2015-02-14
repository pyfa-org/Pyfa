# freighterSMACapacityBonusO1
#
# Used by:
# Ship: Bowhead
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("ORE Freighter").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusO2")*level,
                           stackingPenalties = True)
