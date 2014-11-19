# archaeologySkillVirusBonus
#
# Used by:
# Modules named like: Emission Scope Sharpener (8 of 8)
# Implant: Poteque 'Prospector' Archaeology AC-905
# Implant: Poteque 'Prospector' Environmental Analysis EY-1005
# Skill: Archaeology
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Archaeology"),
                                     "virusCoherence", container.getModifiedItemAttr("virusCoherenceBonus") * level)
