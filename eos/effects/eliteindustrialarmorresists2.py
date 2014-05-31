# Used by:
# Ship: Impel
# Ship: Occator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("armor{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusIndustrial2") * level)
