# eliteBonusJumpFreighterHullHP1
#
# Used by:
# Ships from group: Jump Freighter (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("hp", ship.getModifiedItemAttr("eliteBonusJumpFreighter1"), skill="Jump Freighters")
