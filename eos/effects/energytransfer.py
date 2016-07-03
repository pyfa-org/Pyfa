# Not used by any item
type = "projected", "active"
def handler(fit, module, context):
    if "projected" in context:
        amount = module.getModifiedItemAttr("powerTransferAmount")
        duration = module.getModifiedItemAttr("duration")
        fit.addDrain(duration, -amount, 0)
