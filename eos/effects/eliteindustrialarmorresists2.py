# eliteIndustrialArmorResists2
#
# Used by:
# Ship: Impel
# Ship: Occator
type = "passive"
def handler(fit, ship, context):
        fit.ship.boostItemAttr("armor{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusIndustrial2"), skill="Transport Ships")
