# subSystemBonusMinmatarOffensiveCommandBursts
#
# Used by:
# Subsystem: Loki Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "war"
                                  "fareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
