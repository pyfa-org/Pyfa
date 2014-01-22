# Used by:
# Variations of ship: Nereus (2 of 2)
# Ship: Iteron Mark V
# Ship: Miasmos Amastris Edition
# Ship: Miasmos Quafe Ultra Edition
# Ship: Miasmos Quafe Ultramarine Edition
# Ship: Occator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    # TODO: investigate if we can live without such ifs or hardcoding
    # Viator doesn't have GI bonus
    if "shipBonusGI" in fit.ship.item.attributes:
        bonusAttr = "shipBonusGI"
    else:
        bonusAttr = "shipBonusGI2"
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr(bonusAttr) * level)
