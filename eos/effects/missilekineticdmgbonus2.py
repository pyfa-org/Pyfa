# Used by:
# Skill: Auto-Targeting Missiles
# Skill: Cruise Missiles
# Skill: Heavy Assault Missiles
# Skill: Heavy Missiles
# Skill: Light Missiles
# Skill: Rockets
# Skill: Torpedoes
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                    "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
