# Interceptor2ShieldResist
#
# Used by:
# Ship: Raptor
type = "passive"
def handler(fit, ship, context):
    damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
    for damageType in damageTypes:
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("eliteBonusInterceptor2"), skill="Interceptors")
