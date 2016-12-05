# subsystemBonusAmarrDefensiveArmorResistance
#
# Used by:
# Subsystem: Legion Defensive - Adaptive Augmenter
type = "passive"


def handler(fit, module, context):
    for damage_type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damage_type),
                               module.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                               skill="Amarr Defensive Systems")
