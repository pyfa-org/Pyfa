# Interceptor2ShieldResist
#
# Used by:
# Ship: Raptor
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interceptors").level
    damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
    for damageType in damageTypes:
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("eliteBonusInterceptor2") * level)
