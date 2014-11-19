# eliteBonusGunshipDroneCapacity2
#
# Used by:
# Ship: Ishkur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Assault Frigates").level
    fit.ship.increaseItemAttr("droneCapacity", ship.getModifiedItemAttr("eliteBonusGunship2") * level)