# Used by:
# Modules named like: Particle Dispersion Augmentor (8 of 8)
# Skill: Signal Dispersion
type = "passive"
def handler(fit, container, context):
    groups = ("ECM", "ECM Burst")
    level = container.level if "skill" in context else 1
    for scanType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                      "scan{0}StrengthBonus".format(scanType), container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level,
                                      stackingPenalties = False if "skill" in context else True)
