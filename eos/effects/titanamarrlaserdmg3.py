# Used by:
# Ship: Avatar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Titan").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanAmarrBonus3") * level)
