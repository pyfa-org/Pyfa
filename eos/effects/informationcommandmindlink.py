# informationCommandMindlink
#
# Used by:
# Implant: Caldari Navy Command Mindlink
# Implant: Imperial Navy Command Mindlink
# Implant: Information Command Mindlink
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Modifier", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Modifier", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Modifier", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Modifier", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration", src.getModifiedItemAttr("mindlinkBonus"))
