# Used by:
# Ship: Vigil
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF") * level)
