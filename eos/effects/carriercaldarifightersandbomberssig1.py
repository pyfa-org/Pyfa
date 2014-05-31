# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Carrier").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters") or drone.item.requiresSkill("Fighter Bombers"),
                                 "signatureRadius", ship.getModifiedItemAttr("carrierCaldariBonus1") * level)
