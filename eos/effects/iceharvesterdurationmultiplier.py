# iceHarvesterDurationMultiplier
#
# Used by:
# Variations of ship: Procurer (2 of 2)
# Variations of ship: Retriever (2 of 2)
# Ship: Endurance
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                     "duration", ship.getModifiedItemAttr("iceHarvestCycleBonus"))
