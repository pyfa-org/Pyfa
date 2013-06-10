# Used by:
# Ship: Covetor
type = "passive"
def handler(fit, container, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "duration", container.getModifiedItemAttr("shipBonusORE3") * level)