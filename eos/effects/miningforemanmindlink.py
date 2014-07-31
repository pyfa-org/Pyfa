# Used by:
# Implant: Mining Foreman Mindlink
type = "passive"
def handler(fit, implant, context):
    fit.character.getSkill("Mining Foreman").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", implant.getModifiedItemAttr("mindlinkBonus"))