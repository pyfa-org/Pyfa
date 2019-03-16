# subsystemBonusMinmatarOffensive1HMLHAMVelo
#
# Used by:
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles") or mod.charge.requiresSkill("Heavy Assault Missiles"),
                                  "maxVelocity", container.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                  skill="Minmatar Offensive Systems")
