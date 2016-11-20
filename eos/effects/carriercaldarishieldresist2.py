# carrierCaldariShieldResist2
#
# Used by:
# Ship: Chimera
# Ship: Wyvern
type = "passive"


def handler(fit, ship, context):
    for resType in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(resType),
                               ship.getModifiedItemAttr("carrierCaldariBonus2"), skill="Caldari Carrier")
