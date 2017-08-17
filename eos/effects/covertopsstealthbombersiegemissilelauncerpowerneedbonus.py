# covertOpsStealthBomberSiegeMissileLauncerPowerNeedBonus
#
# Used by:
# Ships from group: Stealth Bomber (4 of 5)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                     "power", ship.getModifiedItemAttr("stealthBomberLauncherPower"))
