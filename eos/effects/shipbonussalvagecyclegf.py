# shipBonusSalvageCycleGF
#
# Used by:
# Ship: Imicus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusGF"), skill="Amarr Frigate")
