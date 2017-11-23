# subsystemEnergyNeutFittingReduction
#
# Used by:
# Subsystem: Legion Core - Energy Parasitic Complex
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
    "cpu", src.getModifiedItemAttr("subsystemEnergyNeutFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
                                  "power", src.getModifiedItemAttr("subsystemEnergyNeutFittingReduction"))
