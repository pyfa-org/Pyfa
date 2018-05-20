# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", module.getModifiedItemAttr("subsystemBonusAmarrOffensive"),
                                  skill="Amarr Offensive Systems")
