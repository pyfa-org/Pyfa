# Used by:
# Skill: Armor Rigging
# Skill: Astronautics Rigging
# Skill: Drones Rigging
# Skill: Electronic Superiority Rigging
# Skill: Energy Weapon Rigging
# Skill: Hybrid Weapon Rigging
# Skill: Launcher Rigging
# Skill: Projectile Weapon Rigging
# Skill: Shield Rigging
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "drawback", skill.getModifiedItemAttr("rigDrawbackBonus") * skill.level)
    