# minigameVirusStrengthBonus
#
# Used by:
# Ships from group: Covert Ops (5 of 5)
# Ships named like: Stratios (2 of 2)
# Subsystems named like: Electronics Emergent Locus Analyzer (4 of 4)
# Ship: Astero
# Ship: Heron
# Ship: Imicus
# Ship: Magnate
# Ship: Nestor
# Ship: Probe
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(
        lambda mod: (mod.item.requiresSkill("Hacking") or mod.item.requiresSkill("Archaeology")),
        "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
