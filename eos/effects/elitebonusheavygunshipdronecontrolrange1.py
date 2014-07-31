# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    amount = ship.getModifiedItemAttr("eliteBonusHeavyGunship1") * level
    fit.extraAttributes.increase("droneControlRange", amount)
