# hackingSkillVirusBonus
#
# Used by:
# Modules named like: Memetic Algorithm Bank (8 of 8)
# Implant: Neural Lace 'Blackglass' Net Intrusion 920-40
# Implant: Poteque 'Prospector' Environmental Analysis EY-1005
# Implant: Poteque 'Prospector' Hacking HC-905
# Skill: Hacking
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"),
                                     "virusCoherence", container.getModifiedItemAttr("virusCoherenceBonus") * level)
