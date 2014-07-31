# Used by:
# Variations of ship: Miasmos (3 of 4)
# Variations of ship: Nereus (2 of 2)
# Ship: Iteron Inner Zone Shipping Edition
# Ship: Iteron Mark V
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
