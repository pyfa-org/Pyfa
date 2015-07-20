# shipMissileSpeedBonusCF
#
# Used by:
# Ship: Buzzard
# Ship: Hawk
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
