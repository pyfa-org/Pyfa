# shipBonusArmorResistAB
#
# Used by:
# Ship: Abaddon
# Ship: Nestor
type = "passive"


def handler(fit, ship, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(type), ship.getModifiedItemAttr("shipBonusAB"),
                               skill="Amarr Battleship")
