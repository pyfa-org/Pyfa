# Used by:
# Ships from group: Industrial (8 of 21)
# Variations of ship: Miasmos (4 of 4)
# Ship: Occator
# Ship: Viator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Industrial").level
    # TODO: investigate if we can live without such ifs or hardcoding
    # Viator doesn't have GI bonus
    if "shipBonusGI" in fit.ship.item.attributes:
        bonusAttr = "shipBonusGI"
    else:
        bonusAttr = "shipBonusGI2"
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr(bonusAttr) * level)
