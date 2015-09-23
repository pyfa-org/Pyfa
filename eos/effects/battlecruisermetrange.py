# battlecruiserMETRange
#
# Used by:
# Ships named like: Harbinger (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "falloff", ship.getModifiedItemAttr("roleBonusCBC"))
