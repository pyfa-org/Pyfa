# Used by:
# Ship: Noctis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("ORE Industrial").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusOreIndustrial1") * level)
