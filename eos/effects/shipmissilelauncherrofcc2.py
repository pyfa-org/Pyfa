# shipMissileLauncherRofCC2
#
# Used by:
# Ship: Onyx
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
