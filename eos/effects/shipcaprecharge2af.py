# Used by:
# Ship: Anathema
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("shipBonus2AF") * level)
