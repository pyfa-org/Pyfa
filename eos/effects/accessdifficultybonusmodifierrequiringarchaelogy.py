# Used by:
# Modules named like: Emission Scope Sharpener (8 of 8)
# Implant: Poteque 'Prospector' Archaeology AC-905
# Implant: Poteque 'Prospector' Environmental Analysis EY-1005
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemIncrease(lambda module: module.item.requiresSkill("Archaeology"),
                                     "accessDifficultyBonus",
                                     container.getModifiedItemAttr("accessDifficultyBonusModifier"), position="post")
