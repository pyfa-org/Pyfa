# emergencyHullEnergizer
#
# Used by:
# Variations of module: Capital Emergency Hull Energizer I (5 of 5)
type = "active"
runtime = "late"


def handler(fit, src, context):
    for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
        fit.ship.multiplyItemAttr('{}DamageResonance'.format(dmgType),
                                  src.getModifiedItemAttr("hull{}DamageResonance".format(dmgType.title())),
                                  stackingPenalties=True, penaltyGroup="postMul")
