# shipHybridRange1CD1
#
# Used by:
# Ship: Cormorant
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCD1") * level)
