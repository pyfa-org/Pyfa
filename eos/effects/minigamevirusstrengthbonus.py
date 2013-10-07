# Used by:
# Ships from group: Covert Ops (5 of 5)
# Ships from group: Frigate (10 of 43)
# Subsystems named like: Electronics Emergent Locus Analyzer (4 of 4)
# Ship: Stratios
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Archaeology"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
