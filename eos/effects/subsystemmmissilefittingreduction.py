type = "passive"
def handler(fit, src, context):
    groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "cpu", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "power", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))
