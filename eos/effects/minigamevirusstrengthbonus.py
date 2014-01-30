# Used by:
# Ships from group: Covert Ops (5 of 5)
# Ship: Astero
# Ship: Heron
# Ship: Imicus
# Ship: Inner Zone Shipping Imicus
# Ship: Magnate
# Ship: Nestor
# Ship: Probe
# Ship: Sarum Magnate
# Ship: Stratios
# Ship: Stratios Emergency Responder
# Ship: Sukuuvestaa Heron
# Ship: Tash-Murkon Magnate
# Ship: Vherokior Probe
# Subsystem: Legion Electronics - Emergent Locus Analyzer
# Subsystem: Loki Electronics - Emergent Locus Analyzer
# Subsystem: Proteus Electronics - Emergent Locus Analyzer
# Subsystem: Tengu Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Archaeology"),
                                     "virusStrength", container.getModifiedItemAttr("virusStrengthBonus") * level)
