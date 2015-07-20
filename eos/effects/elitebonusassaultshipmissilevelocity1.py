# eliteBonusAssaultShipMissileVelocity1
#
# Used by:
# Ship: Hawk
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")