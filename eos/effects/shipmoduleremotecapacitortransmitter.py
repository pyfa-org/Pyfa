# shipModuleRemoteCapacitorTransmitter
#
# Used by:
# Modules from group: Remote Capacitor Transmitter (41 of 41)
from eos.modifiedAttributeDict import ModifiedAttributeDict
type = "projected", "active"


def handler(fit, src, context, **kwargs):
    if "projected" in context:
        amount = src.getModifiedItemAttr("powerTransferAmount")
        duration = src.getModifiedItemAttr("duration")

        if 'effect' in kwargs:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        fit.addDrain(src, duration, -amount, 0)
