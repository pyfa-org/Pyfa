# carrierCaldariFightersAndBombersSig1
#
# Used by:
# Ship: Revenant
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(
        lambda drone: drone.item.requiresSkill("Fighters") or drone.item.requiresSkill("Fighter Bombers"),
        "signatureRadius", ship.getModifiedItemAttr("carrierCaldariBonus1"), skill="Caldari Carrier")
