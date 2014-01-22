# Used by:
# Modules named like: Particle Dispersion Projector (8 of 8)
# Implant: Low-grade Centurion Alpha
# Implant: Low-grade Centurion Beta
# Implant: Low-grade Centurion Delta
# Implant: Low-grade Centurion Epsilon
# Implant: Low-grade Centurion Gamma
# Skill: Long Distance Jamming
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                  stackingPenalties = "skill" not in context and "implant" not in context)
