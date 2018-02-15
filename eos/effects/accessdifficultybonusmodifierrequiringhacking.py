# accessDifficultyBonusModifierRequiringHacking
#
# Used by:
# Modules named like: Memetic Algorithm Bank (8 of 8)
# Implant: Neural Lace 'Blackglass' Net Intrusion 920-40
# Implant: Poteque 'Prospector' Environmental Analysis EY-1005
# Implant: Poteque 'Prospector' Hacking HC-905
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemIncrease(lambda c: c.item.requiresSkill("Hacking"),
                                     "accessDifficultyBonus",
                                     container.getModifiedItemAttr("accessDifficultyBonusModifier"), position="post")
