# Used by:
# Ship: Drake Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battlecruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCBC1") * level)
