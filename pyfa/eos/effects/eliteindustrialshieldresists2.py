# eliteIndustrialShieldResists2
#
# Used by:
# Ship: Bustard
# Ship: Mastodon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusIndustrial2") * level)
