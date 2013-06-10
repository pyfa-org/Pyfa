# Used by:
# Ship: Nyx
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Carrier").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighter Bombers"),
                                 "damageMultiplier", ship.getModifiedItemAttr("carrierGallenteBonus2") * level)
