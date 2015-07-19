# shipBonusORECapShipDroneArmorHPAndShieldHPAndHpBonus
#
# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusORECapital4"), skill="Capital Industrial Ships")
