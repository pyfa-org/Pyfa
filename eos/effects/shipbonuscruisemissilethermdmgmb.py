# Used by:
# Ship: Typhoon Fleet Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusMB") * level)
