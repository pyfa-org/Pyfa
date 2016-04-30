# remoteEnergyTransferFalloff
#
# Used by:
# Modules from group: Remote Capacitor Transmitter (41 of 41)
type = "projected", "active"
def handler(fit, module, context):
    if "projected" in context:
        amount = module.getModifiedItemAttr("maxRange")
        duration = module.getModifiedItemAttr("duration")
        fit.addDrain(duration, -amount, 0)
