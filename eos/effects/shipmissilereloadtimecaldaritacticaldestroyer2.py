# shipMissileReloadTimeCaldariTacticalDestroyer2
#
# Used by:
# Ship: Jackdaw
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "reloadTime", ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari2"), skill="Caldari Tactical Destroyer")
