# Used by:
# Modules from group: Rig Resource Processing (8 of 10)
# Implant: Poteque 'Prospector' Salvaging SV-905
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "accessDifficultyBonus", container.getModifiedItemAttr("accessDifficultyBonus"), position="post")
