# Used by:
# Ships from group: Capital Industrial Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    if fit.extraAttributes["siege"]:
        level = fit.character.getSkill("Capital Industrial Ships").level
        fit.ship.increaseItemAttr("commandBonusEffective", ship.getModifiedItemAttr("shipBonusORECapital2") * level)
