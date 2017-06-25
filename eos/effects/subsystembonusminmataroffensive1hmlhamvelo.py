# subsystemBonusMinmatarOffensive1HMLHAMVelo
#
# Used by:
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Heavy Missiles") or mod.item.requiresSkill("Heavy Assault Missiles"),
                                  "maxVelocity", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                  skill="Minmatar Offensive Systems")
