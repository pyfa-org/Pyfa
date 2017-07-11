# subsystemBonusGallenteCoreCapacitorRecharge
#
# Used by:
# Subsystem: Proteus Core - Augmented Fusion Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("rechargeRate", src.getModifiedItemAttr("subsystemBonusGallenteCore"),
                           skill="Gallente Core Systems")
