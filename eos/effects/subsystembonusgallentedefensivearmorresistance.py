# subsystemBonusGallenteDefensiveArmorResistance
#
# Used by:
# Subsystem: Proteus Defensive - Adaptive Augmenter
type = "passive"
def handler(fit, module, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(type),
                               module.getModifiedItemAttr("subsystemBonusGallenteDefensive"), skill="Gallente Defensive Systems")
