# passiveSpeedLimit
#
# Used by:
# Modules from group: Entosis Link (2 of 2)
runtime = "late"
type = "passive"
def handler(fit, src, context):
    fit.extraAttributes['speedLimit'] = src.getModifiedItemAttr("speedLimit")
