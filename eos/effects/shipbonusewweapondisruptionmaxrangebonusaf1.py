# Used by:
# Ship: Crucifier
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "maxRangeBonus", ship.getModifiedItemAttr("shipBonusAF") * level)
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "falloffBonus", ship.getModifiedItemAttr("shipBonusAF") * level)
