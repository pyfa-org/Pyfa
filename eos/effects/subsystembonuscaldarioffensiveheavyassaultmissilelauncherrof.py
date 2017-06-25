# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", module.getModifiedItemAttr("subsystemBonusCaldariOffensive"),
                                  skill="Caldari Offensive Systems")
