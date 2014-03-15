# Used by:
# Ship: Impairor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "maxRangeBonus", ship.getModifiedItemAttr("rookieWeaponDisruptionBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "falloffBonus", ship.getModifiedItemAttr("rookieWeaponDisruptionBonus"))
