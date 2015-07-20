# shipBonusSalvageCycleMF
#
# Used by:
# Ship: Probe
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
