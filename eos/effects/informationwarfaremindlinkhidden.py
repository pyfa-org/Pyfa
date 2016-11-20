# informationWarfareMindlinkHidden
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
# Implant: Information Warfare Mindlink
type = "passive"


def handler(fit, implant, context):
    fit.character.getSkill("Information Command").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"),
                                  "commandBonusHidden", implant.getModifiedItemAttr("mindlinkBonus"))
