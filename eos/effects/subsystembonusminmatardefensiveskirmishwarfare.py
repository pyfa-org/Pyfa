# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
