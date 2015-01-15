# shipBonusThermalMissileDamageGB2
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusGB2") * level)
