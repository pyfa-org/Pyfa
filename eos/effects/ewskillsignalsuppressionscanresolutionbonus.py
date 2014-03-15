# Used by:
# Modules named like: Inverted Signal Field Projector (8 of 8)
# Skill: Signal Suppression
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    penalized = False if "skill" in context else True
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "scanResolutionBonus", container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level,
                                  stackingPenalties=penalized)
