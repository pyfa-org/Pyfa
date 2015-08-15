# shipMissileVelocityCF
#
# Used by:
# Ship: Crow
# Ship: Kestrel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
