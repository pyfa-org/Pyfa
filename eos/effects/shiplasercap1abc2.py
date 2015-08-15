# shipLaserCap1ABC2
#
# Used by:
# Ship: Absolution
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusABC2"), skill="Amarr Battlecruiser")
