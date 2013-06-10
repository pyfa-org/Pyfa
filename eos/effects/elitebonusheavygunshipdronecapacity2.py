# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.ship.increaseItemAttr("droneCapacity", ship.getModifiedItemAttr("eliteBonusHeavyGunship2") * level)
