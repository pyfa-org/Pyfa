# subsystemBonusMinmatarCoreCapacitorRecharge
#
# Used by:
# Subsystem: Loki Core - Augmented Nuclear Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("rechargeRate", src.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                           skill="Minmatar Core Systems")
