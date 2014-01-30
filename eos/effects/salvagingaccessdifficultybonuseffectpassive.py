# Used by:
# Modules named like: Salvage (8 of 8)
# Implant: Poteque 'Prospector' Salvaging SV-905
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "accessDifficultyBonus", container.getModifiedItemAttr("accessDifficultyBonus"), position="post")
