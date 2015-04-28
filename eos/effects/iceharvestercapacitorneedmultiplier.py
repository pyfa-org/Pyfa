# iceHarvesterCapacitorNeedMultiplier
#
# Used by:
# Variations of ship: Procurer (2 of 2)
# Variations of ship: Retriever (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                     "capacitorNeed", ship.getModifiedItemAttr("iceHarvestCycleBonus"))
