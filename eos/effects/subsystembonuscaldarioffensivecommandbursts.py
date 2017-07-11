# subSystemBonusCaldariOffensiveCommandBursts
#
# Used by:
# Subsystem: Tengu Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
