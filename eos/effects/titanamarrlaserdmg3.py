# titanAmarrLaserDmg3
#
# Used by:
# Ship: Avatar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanAmarrBonus3"), skill="Amarr Titan")
