# shipBonusIceHarvesterDurationORE3
#
# Used by:
# Ships from group: Exhumer (3 of 3)
# Ships from group: Mining Barge (3 of 3)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "duration", container.getModifiedItemAttr("shipBonusORE3"), skill="Mining Barge")