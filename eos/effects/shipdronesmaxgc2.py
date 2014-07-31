# Used by:
# Ship: Guardian-Vexor
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    amount = ship.getModifiedItemAttr("shipBonusGC2")
    fit.extraAttributes.increase("maxActiveDrones", amount * level)
