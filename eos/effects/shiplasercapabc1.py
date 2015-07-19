# shipLaserCapABC1
#
# Used by:
# Ship: Harbinger
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC1"), skill="Amarr Battlecruiser")
