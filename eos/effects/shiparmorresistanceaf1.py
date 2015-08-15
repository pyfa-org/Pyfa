# shipArmorResistanceAF1
#
# Used by:
# Ship: Malediction
type = "passive"
def handler(fit, ship, context):
    damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
    for damageType in damageTypes:
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
