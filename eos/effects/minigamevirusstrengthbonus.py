# Used by:
# Ships from group: Covert Ops (5 of 5)
# Ships named like: Stratios (2 of 2)
# Subsystems named like: Electronics Emergent Locus Analyzer (4 of 4)
# Variations of ship: Heron (3 of 3)
# Variations of ship: Imicus (3 of 3)
# Variations of ship: Magnate (4 of 6)
# Variations of ship: Probe (3 of 3)
# Ship: Astero
# Ship: Nestor
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Archaeology"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
