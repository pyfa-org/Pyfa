# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.ship.increaseItemAttr("droneCapacity", ship.getModifiedItemAttr("eliteBonusCommandShips1") * level)
