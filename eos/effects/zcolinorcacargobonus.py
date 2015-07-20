# zColinOrcaCargoBonus
#
# Used by:
# Ship: Orca
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipOrcaCargoBonusOrca1"), skill="Industrial Command Ships")
