# Used by:
# Ships named like: Iteron Mark (7 of 7)
# Variations of ship: Iteron (2 of 2)
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
