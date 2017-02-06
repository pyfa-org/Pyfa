# freighterSMACapacityBonusO1
#
# Used by:
# Ship: Bowhead
type = "passive"


def handler(fit, ship, context):
    # todo: stacking?
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusO2"), skill="ORE Freighter",
                           stackingPenalties=True)
