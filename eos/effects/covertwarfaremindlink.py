# covertWarfareMindlink
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
# Implant: Information Warfare Mindlink
type = "passive"


def handler(fit, implant, context):
    fit.character.getSkill("Information Warfare").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))
