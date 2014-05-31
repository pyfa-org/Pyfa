# Used by:
# Ships named like: Punisher (3 of 3)
# Ship: Astero
# Ship: Malice
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.ship.boostItemAttr("armorKineticDamageResonance", ship.getModifiedItemAttr("shipBonusAF") * level)
