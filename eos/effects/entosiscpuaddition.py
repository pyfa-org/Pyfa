# entosisCPUAddition
#
# Used by:
# Modules from group: Entosis Link (2 of 2)
type = "passive"
def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("entosisCPUAdd"))

