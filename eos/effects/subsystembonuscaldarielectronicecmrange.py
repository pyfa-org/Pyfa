# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariElectronic"),
                                  skill="Caldari Electronic Systems")
