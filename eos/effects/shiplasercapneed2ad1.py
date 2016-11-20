# shipLaserCapNeed2AD1
#
# Used by:
# Ship: Coercer
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
