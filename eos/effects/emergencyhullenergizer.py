type = "active"
runtime = "late"


def handler(fit, src, context):
    for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
        fit.ship.forceItemAttr('{}DamageResonance'.format(dmgType), src.getModifiedItemAttr("hull{}DamageResonance".format(dmgType.title())))
