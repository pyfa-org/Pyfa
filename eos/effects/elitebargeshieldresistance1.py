# Used by:
# Ships from group: Exhumer (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Exhumers").level
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.ship.boostItemAttr("shield{}DamageResonance".format(damageType.capitalize()),
                               ship.getModifiedItemAttr("eliteBonusBarge1") * level)
