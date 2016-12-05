# Not used by any item
type = "passive"


def handler(fit, implant, context):
    fit.character.getSkill("Information Command").suppress()
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"),
                                  "commandBonusHidden", implant.getModifiedItemAttr("mindlinkBonus"))
