# energyNosferatuFalloff
#
# Used by:
# Modules from group: Energy Nosferatu (51 of 51)
type = "active", "projected"
runTime = "late"


def handler(fit, src, context):
    amount = src.getModifiedItemAttr("powerTransferAmount")
    time = src.getModifiedItemAttr("duration")

    if "projected" in context:
        fit.addDrain(src, time, amount, 0)
    elif "module" in context:
        src.itemModifiedAttributes.force("capacitorNeed", -amount)
