# roleBonusFlagCruiserModuleFittingReduction
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Propulsion Module", "Micro Jump Drive"),
                                  "power", src.getModifiedItemAttr("flagCruiserFittingBonusPropMods"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Propulsion Module", "Micro Jump Drive"),
                                  "cpu", src.getModifiedItemAttr("flagCruiserFittingBonusPropMods"))

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Target Painter", "Scan Probe Launcher"),
                                  "cpu", src.getModifiedItemAttr("flagCruiserFittingBonusPainterProbes"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Target Painter", "Scan Probe Launcher"),
                                  "power", src.getModifiedItemAttr("flagCruiserFittingBonusPainterProbes"))
