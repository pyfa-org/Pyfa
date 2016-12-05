# subsystemBonusGallenteDefensiveArmorResistance
#
# Used by:
# Subsystem: Proteus Defensive - Adaptive Augmenter
type = "passive"


def handler(fit, module, context):
    for damage_type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damage_type),
                               module.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                               skill="Gallente Defensive Systems")
