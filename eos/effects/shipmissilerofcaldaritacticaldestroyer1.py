# shipMissileRoFCaldariTacticalDestroyer1
#
# Used by:
# Ship: Jackdaw
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari1") * level)


