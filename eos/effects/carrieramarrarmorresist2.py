# Used by:
# Ship: Aeon
# Ship: Archon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Carrier").level
    for resType in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(resType),
                               ship.getModifiedItemAttr("carrierAmarrBonus2") * level)
