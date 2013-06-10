# Used by:
# Modules from group: CPU Enhancer (27 of 27)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("cpuOutput", module.getModifiedItemAttr("cpuMultiplier"))