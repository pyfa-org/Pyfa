# eliteBonusJumpFreighterShieldHP1
#
# Used by:
# Ship: Nomad
# Ship: Rhea
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("eliteBonusJumpFreighter1"), skill="Jump Freighters")
