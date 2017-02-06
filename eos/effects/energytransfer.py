# Not used by any item
type = "projected", "active"


def handler(fit, src, context):
    if "projected" in context:
        amount = src.getModifiedItemAttr("powerTransferAmount")
        duration = src.getModifiedItemAttr("duration")
        fit.addDrain(src, duration, -amount, 0)
