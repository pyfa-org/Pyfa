# battlecruiserMHTRange
#
# Used by:
# Ships named like: Brutix (2 of 2)
# Ship: Ferox
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("roleBonusCBC"))
