# Not used by any item
type = "passive"
runTime = "early"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", module.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"),
                                  skill="Minmatar Defensive Systems")
