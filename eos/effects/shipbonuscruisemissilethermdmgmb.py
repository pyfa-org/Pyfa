# shipBonusCruiseMissileThermDmgMB
#
# Used by:
# Ship: Typhoon Fleet Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
