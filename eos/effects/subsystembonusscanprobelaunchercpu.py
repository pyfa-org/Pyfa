# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Scan Probe Launcher",
                                  "cpu", module.getModifiedItemAttr("cpuNeedBonus"))
