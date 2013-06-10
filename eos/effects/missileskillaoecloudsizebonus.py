# Used by:
# Implants named like: Zainou 'Deadeye' Guided Missile Precision GP (6 of 6)
# Modules named like: Warhead Rigor Catalyst (8 of 8)
# Skill: Guided Missile Precision
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles") or \
                                                mod.charge.requiresSkill("Rockets") or \
                                                mod.charge.requiresSkill("Heavy Missiles") or \
                                                mod.charge.requiresSkill("Heavy Assault Missiles") or \
                                                mod.charge.requiresSkill("Cruise Missiles") or \
                                                mod.charge.requiresSkill("Torpedoes"),
                                    "aoeCloudSize", container.getModifiedItemAttr("aoeCloudSizeBonus") * level,
                                    stackingPenalties = False)
