# covertOpsStealthBomberSiegeMissileLauncherCPUNeedBonus
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                     "cpu", ship.getModifiedItemAttr("stealthBomberLauncherCPU"))
