# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                     "capacitorNeed", ship.getModifiedItemAttr("iceHarvestCycleBonus"))
