# energyTransfer
#
# Used by:
# Modules from group: Remote Capacitor Transmitter (38 of 38)
type = "projected", "active"
def handler(fit, module, context):
    if "projected" in context:
        amount = module.getModifiedItemAttr("powerTransferAmount")
        duration = module.getModifiedItemAttr("duration")
        fit.addDrain(duration, -amount, 0)
