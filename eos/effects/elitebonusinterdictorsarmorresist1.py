# Used by:
# Ship: Heretic
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interdictors").level
    for damageType in ("Em", "Thermal", "Explosive", "Kinetic"):
        fit.ship.boostItemAttr("armor%sDamageResonance" % damageType,
                               ship.getModifiedItemAttr("eliteBonusInterdictors1") * level)
