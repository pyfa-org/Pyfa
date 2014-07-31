# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Industrial Command Ships").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipOrcaCargoBonusOrca1") * level)
