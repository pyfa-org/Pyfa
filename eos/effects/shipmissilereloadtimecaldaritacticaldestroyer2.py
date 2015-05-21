# shipMissileReloadTimeCaldariTacticalDestroyer2
#
# Used by:
# Ship: Jackdaw
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "reloadTime", ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari2") * level)
