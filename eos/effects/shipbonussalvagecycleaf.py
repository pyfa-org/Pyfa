# shipBonusSalvageCycleAF
#
# Used by:
# Ship: Magnate
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
