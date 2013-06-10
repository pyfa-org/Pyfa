# Used by:
# Ship: Noctis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("ORE Industrial").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusOreIndustrial2") * level)
