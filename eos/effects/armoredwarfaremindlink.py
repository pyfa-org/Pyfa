# armoredWarfareMindlink
#
# Used by:
# Implant: Armored Warfare Mindlink
# Implant: Federation Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
type = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))
