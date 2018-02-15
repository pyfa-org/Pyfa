# moduleBonusAssaultDamageControl
#
# Used by:
# Variations of module: Assault Damage Control I (5 of 5)
type = "active"
runTime = "early"


def handler(fit, src, context):
    for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
        for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
            bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
            bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
            booster = "%s%sDamageResonance" % (layer, damageType)

            src.forceItemAttr(booster, src.getModifiedItemAttr("resistanceMultiplier"))
