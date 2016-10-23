# armoredWarfareMindlink
#
# Used by:
# Implant: Armored Command Mindlink
# Implant: Federation Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))