# Used by:
# Ship: Ares
# Ship: Crow
# Ship: Malediction
# Ship: Stiletto
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interceptors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusInterceptor2") * level)