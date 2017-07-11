# subsystemBonusMinmatarOffensive3MissileExpVelo
#
# Used by:
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                  "aoeVelocity", container.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                  skill="Minmatar Offensive Systems")
