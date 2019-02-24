# skillBombDeploymentModuleReactivationDelayBonus
#
# Used by:
# Skill: Bomb Deployment
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Bomb",
                                  "moduleReactivationDelay", skill.getModifiedItemAttr("reactivationDelayBonus") * skill.level)
