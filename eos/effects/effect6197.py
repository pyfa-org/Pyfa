# energyNosferatuFalloff
#
# Used by:
# Modules from group: Energy Nosferatu (54 of 54)
from eos.modifiedAttributeDict import ModifiedAttributeDict

type = "active", "projected"
runTime = "late"


def handler(fit, src, context, **kwargs):
    amount = src.getModifiedItemAttr("powerTransferAmount")
    time = src.getModifiedItemAttr("duration")

    if 'effect' in kwargs and "projected" in context:
        amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

    if "projected" in context:
        fit.addDrain(src, time, amount, 0)
    elif "module" in context:
        src.itemModifiedAttributes.force("capacitorNeed", -amount)
