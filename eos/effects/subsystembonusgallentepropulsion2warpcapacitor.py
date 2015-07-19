# subsystemBonusGallentePropulsion2WarpCapacitor
#
# Used by:
# Subsystem: Proteus Propulsion - Gravitational Capacitor
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion2"), skill="Gallente Propulsion Systems")
