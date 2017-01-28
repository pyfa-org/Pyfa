# shieldCommandMindlink
#
# Used by:
# Implants from group: Cyber Leadership (4 of 10)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                    src.getModifiedItemAttr("mindlinkBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                  src.getModifiedItemAttr("mindlinkBonus"))
