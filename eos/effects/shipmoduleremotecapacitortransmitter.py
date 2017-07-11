# shipModuleRemoteCapacitorTransmitter
#
# Used by:
# Modules from group: Remote Capacitor Transmitter (41 of 41)
type = "projected", "active"


def handler(fit, src, context):
    if "projected" in context:
        amount = src.getModifiedItemAttr("powerTransferAmount")
        duration = src.getModifiedItemAttr("duration")
        fit.addDrain(src, duration, -amount, 0)
