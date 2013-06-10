# Used by:
# Ship: Orca
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Industrial Command Ships").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipOrcaCargoBonusOrca1") * level)
