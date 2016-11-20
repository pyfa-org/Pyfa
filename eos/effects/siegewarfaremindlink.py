# siegeWarfareMindlink
#
# Used by:
# Implant: Caldari Navy Warfare Mindlink
# Implant: Republic Fleet Warfare Mindlink
# Implant: Siege Warfare Mindlink
type = "passive"


def handler(fit, implant, context):
    fit.character.getSkill("Shield Command Specialist").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))
