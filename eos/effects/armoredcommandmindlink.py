# armoredCommandMindlink
#
# Used by:
# Implant: Armored Command Mindlink
# Implant: Federation Navy Command Mindlink
# Implant: Imperial Navy Command Mindlink
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value", src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration", src.getModifiedItemAttr("mindlinkBonus"))
