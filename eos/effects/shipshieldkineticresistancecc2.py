# shipShieldKineticResistanceCC2
#
# Used by:
# Variations of ship: Moa (3 of 4)
# Ship: 毒蜥级YC117年特别版
# Ship: 银鹰级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCC2") * level)
