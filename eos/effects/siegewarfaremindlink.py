# Used by:
# Implant: Siege Warfare Mindlink
type = "passive"
def handler(fit, implant, context):
    fit.character.getSkill("Siege Warfare Specialist").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))
