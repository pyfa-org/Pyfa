# emergencyHullEnergizer
#
# Used by:
# Variations of module: Capital Emergency Hull Energizer I (5 of 5)
type = "active"
runtime = "late"


def handler(fit, src, context):
    for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
        fit.ship.forceItemAttr('{}DamageResonance'.format(dmgType), src.getModifiedItemAttr("hull{}DamageResonance".format(dmgType.title())))
