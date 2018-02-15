# damageControl
#
# Used by:
# Modules from group: Damage Control (22 of 27)
type = "passive"


def handler(fit, module, context):
    for layer, attrPrefix in (('shield', 'shield'), ('armor', 'armor'), ('hull', '')):
        for damageType in ('Kinetic', 'Thermal', 'Explosive', 'Em'):
            bonus = "%s%sDamageResonance" % (attrPrefix, damageType)
            bonus = "%s%s" % (bonus[0].lower(), bonus[1:])
            booster = "%s%sDamageResonance" % (layer, damageType)
            penalize = False if layer == 'hull' else True
            fit.ship.multiplyItemAttr(bonus, module.getModifiedItemAttr(booster),
                                      stackingPenalties=penalize, penaltyGroup="preMul")
