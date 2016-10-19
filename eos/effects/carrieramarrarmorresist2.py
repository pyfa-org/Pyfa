# carrierAmarrArmorResist2
#
# Used by:
# Ship: Aeon
# Ship: Archon
type = "passive"


def handler(fit, ship, context):
    for resType in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(resType),
                               ship.getModifiedItemAttr("carrierAmarrBonus2"), skill="Amarr Carrier")
