# resistanceKillerHullAll
#
# Used by:
# Modules named like: Polarized (12 of 18)
type = "passive"
def handler(fit, module, context):
    for dmgType in ('em', 'thermal', 'kinetic', 'explosive'):
        tgtAttr = '{}DamageResonance'.format(dmgType)
        fit.ship.forceItemAttr(tgtAttr, module.getModifiedItemAttr("resistanceKillerHull"))
