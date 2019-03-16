# eliteBonusInterdictorsArmorResist1
#
# Used by:
# Ship: Heretic
type = "passive"


def handler(fit, ship, context):
    for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
        fit.ship.boostItemAttr("armor%sDamageResonance" % damageType,
                               ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")
