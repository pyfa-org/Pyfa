# shipMissileLauncherSpeedBonusMC2
#
# Used by:
# Ship: Bellicose
type = "passive"
def handler(fit, ship, context):
    groups = ("Missile Launcher Rapid Light", "Missile Launcher Heavy", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
