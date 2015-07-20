# eliteBonusJumpFreighterJumpDriveConsumptionAmount2
#
# Used by:
# Ships from group: Jump Freighter (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("jumpDriveConsumptionAmount", ship.getModifiedItemAttr("eliteBonusJumpFreighter2"), skill="Jump Freighters")
