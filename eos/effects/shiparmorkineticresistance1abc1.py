# shipArmorKineticResistance1ABC1
#
# Used by:
# Variations of ship: Prophecy (2 of 2)
# Ship: Absolution
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battlecruiser").level
    fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusABC1") * level)
