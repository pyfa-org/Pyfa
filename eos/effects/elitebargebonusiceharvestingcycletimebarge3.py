# eliteBargeBonusIceHarvestingCycleTimeBarge3
#
# Used by:
# Ships from group: Exhumer (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Exhumers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "duration", ship.getModifiedItemAttr("eliteBonusBarge2") * level)
