# shipBonusSalvageCycleGF
#
# Used by:
# Ship: Imicus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusGF") * level)
