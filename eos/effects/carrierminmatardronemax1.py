# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Carrier").level
    amount = ship.getModifiedItemAttr("carrierMinmatarBonus1")
    fit.extraAttributes.increase("maxActiveDrones", amount * level)
