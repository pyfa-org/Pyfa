# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "falloffEffectiveness", src.getModifiedItemAttr("shipBonusORECapital3"),
                                  skill="Capital Industrial Ships")
