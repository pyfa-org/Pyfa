# structureHPBonusAddPassive
#
# Used by:
# Subsystems named like: Defensive Covert Reconfiguration (4 of 4)
# Subsystem: Loki Defensive - Adaptive Defense Node
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("hp", module.getModifiedItemAttr("structureHPBonusAdd") or 0)
