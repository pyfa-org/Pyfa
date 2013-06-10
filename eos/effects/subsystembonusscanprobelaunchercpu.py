# Used by:
# Subsystems named like: Electronics Emergent Locus Analyzer (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Scan Probe Launcher",
                                  "cpu", module.getModifiedItemAttr("cpuNeedBonus"))
