# skirmishCommandMindlink
#
# Used by:
# Implant: Federation Navy Command Mindlink
# Implant: Republic Fleet Command Mindlink
# Implant: Skirmish Command Mindlink
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration", src.getModifiedItemAttr("mindlinkBonus"))
