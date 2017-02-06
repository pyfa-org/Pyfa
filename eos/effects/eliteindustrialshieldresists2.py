# eliteIndustrialShieldResists2
#
# Used by:
# Ship: Bustard
# Ship: Mastodon
type = "passive"


def handler(fit, ship, context):
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusIndustrial2"), skill="Transport Ships")
