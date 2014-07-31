# Used by:
# Ships from group: Exhumer (3 of 4)
# Ship: Procurer
# Ship: Retriever
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                     "duration", ship.getModifiedItemAttr("iceHarvestCycleBonus"))
