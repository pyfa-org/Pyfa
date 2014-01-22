# Used by:
# Ship: Gila
# Ship: Ishtar
# Ship: Stratios
# Ship: Stratios Emergency Responder
# Ship: Vexor
# Ship: Vexor Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusGC2") * level)
