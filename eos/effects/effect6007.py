# shipSETCapNeedAmarrTacticalDestroyer2
#
# Used by:
# Ship: Confessor
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr2"),
                                  skill="Amarr Tactical Destroyer")
