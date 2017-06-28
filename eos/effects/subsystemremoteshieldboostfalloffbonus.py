type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Shield Booster", "Ancillary Remote Shield Booster"),
                                  "falloffEffectiveness", src.getModifiedItemAttr("remoteShieldBoosterFalloffBonus"))
