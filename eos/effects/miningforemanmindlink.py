# miningForemanMindlink
#
# Used by:
# Implant: Mining Foreman Mindlink
# Implant: ORE Mining Director Mindlink
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration", src.getModifiedItemAttr("mindlinkBonus"))
