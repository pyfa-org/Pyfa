# shipHybridDamageBonusCBC2
#
# Used by:
# Ship: Naga
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")
