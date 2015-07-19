# titanGallenteHybridDamage1
#
# Used by:
# Ship: Erebus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanGallenteBonus1"), skill="Gallente Titan")
