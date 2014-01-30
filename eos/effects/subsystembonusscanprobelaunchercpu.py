# Used by:
# Subsystem: Legion Electronics - Emergent Locus Analyzer
# Subsystem: Loki Electronics - Emergent Locus Analyzer
# Subsystem: Proteus Electronics - Emergent Locus Analyzer
# Subsystem: Tengu Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Scan Probe Launcher",
                                  "cpu", module.getModifiedItemAttr("cpuNeedBonus"))
