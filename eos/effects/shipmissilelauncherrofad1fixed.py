# shipMissileLauncherRoFAD1Fixed
#
# Used by:
# Ship: Heretic
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")