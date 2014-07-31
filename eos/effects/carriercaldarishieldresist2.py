# Used by:
# Ship: Chimera
# Ship: Wyvern
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Carrier").level
    for resType in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(resType),
                               ship.getModifiedItemAttr("carrierCaldariBonus2") * level)
