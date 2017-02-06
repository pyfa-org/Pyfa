# subsystemBonusMinmatarDefensiveArmorResistance
#
# Used by:
# Subsystem: Loki Defensive - Adaptive Augmenter
type = "passive"


def handler(fit, module, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(type),
                               module.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                               skill="Minmatar Defensive Systems")
