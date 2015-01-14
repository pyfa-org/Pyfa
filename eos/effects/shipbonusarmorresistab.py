# shipBonusArmorResistAB
#
# Used by:
# Ships named like: Abaddon (3 of 3)
# Ship: Nestor
# Ship: 地狱天使级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(type), ship.getModifiedItemAttr("shipBonusAB") * level)
