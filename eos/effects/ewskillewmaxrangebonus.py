# Used by:
# Implants named like: Low grade Centurion (5 of 6)
# Modules named like: Particle Dispersion Projector (8 of 8)
# Skill: Long Distance Jamming
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level,
                                  stackingPenalties = "skill" not in context and "implant" not in context)
