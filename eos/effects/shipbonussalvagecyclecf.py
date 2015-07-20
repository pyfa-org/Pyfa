# shipBonusSalvageCycleCF
#
# Used by:
# Ship: Heron
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
