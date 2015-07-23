# eliteIndustrialArmorResists2
#
# Used by:
# Ship: Impel
# Ship: Occator
type = "passive"
def handler(fit, ship, context):
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("armor{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusIndustrial2"), skill="Transport Ships")
