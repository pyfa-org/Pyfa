# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic"),
                                  skill="Minmatar Electronic Systems")
