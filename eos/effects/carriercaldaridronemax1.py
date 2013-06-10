# Used by:
# Ship: Chimera
# Ship: Revenant
# Ship: Wyvern
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Carrier").level
    amount = ship.getModifiedItemAttr("carrierCaldariBonus1")
    fit.extraAttributes.increase("maxActiveDrones", amount * level)
