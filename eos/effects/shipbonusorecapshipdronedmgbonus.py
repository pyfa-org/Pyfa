# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Capital Industrial Ships").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusORECapital4") * level)
