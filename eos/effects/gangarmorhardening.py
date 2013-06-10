# Used by:
# Variations of module: Armored Warfare Link - Passive Defense I (2 of 2)
type = "gang", "active"
gangBoost = "armorResistance"
def handler(fit, module, context):
    if "gang" not in context: return
    for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
        fit.ship.boostItemAttr("armor%sDamageResonance" % damageType,
                               module.getModifiedItemAttr("commandBonus"),
                               stackingPenalties = True)
