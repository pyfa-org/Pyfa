# shipVelocityBonusMI
#
# Used by:
# Variations of ship: Mammoth (2 of 2)
# Ship: Hoarder
# Ship: Mammoth Nefantar Edition
# Ship: Prowler
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Industrial").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusMI") * level)
