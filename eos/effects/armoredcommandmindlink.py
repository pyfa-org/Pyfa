# armoredCommandMindlink
#
# Used by:
# Implant: Armored Command Mindlink
# Implant: Federation Navy Command Mindlink
# Implant: Imperial Navy Command Mindlink
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                  src.getModifiedItemAttr("mindlinkBonus"))
