# shipLaserRofAC2
#
# Used by:
# Ship: Omen
# Ship: Zealot
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
