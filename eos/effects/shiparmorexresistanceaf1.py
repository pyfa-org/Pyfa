# Used by:
# Ships named like: Punisher (2 of 2)
# Ship: Astero
# Ship: Malice
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusAF") * level)
