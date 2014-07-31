# Used by:
# Ship: Erebus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Titan").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanGallenteBonus1") * level)
