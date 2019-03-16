# shipMaxLockedTargetsBonusAddPassive
#
# Used by:
# Subsystems named like: Core Dissolution Sequencer (2 of 2)
# Subsystems named like: Core Electronic Efficiency Gate (2 of 2)
# Subsystems named like: Offensive Support Processor (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargetsBonus"))
