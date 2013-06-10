# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    if fit.extraAttributes["siege"]:
        level = fit.character.getSkill("Capital Industrial Ships").level
        fit.ship.increaseItemAttr("commandBonusEffective", ship.getModifiedItemAttr("shipBonusORECapital2") * level)
