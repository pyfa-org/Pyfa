# Used by:
# Implant: Federation Navy Warfare Mindlink
# Implant: Republic Fleet Warfare Mindlink
# Implant: Skirmish Warfare Mindlink
type = "passive"
def handler(fit, implant, context):
    fit.character.getSkill("Skirmish Warfare Specialist").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))
