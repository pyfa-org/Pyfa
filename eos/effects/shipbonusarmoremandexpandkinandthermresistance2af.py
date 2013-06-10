# Used by:
# Ship: Malediction
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
    for damageType in damageTypes:
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("shipBonus2AF") * level)
