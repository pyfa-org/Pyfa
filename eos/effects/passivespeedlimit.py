# passiveSpeedLimit
#
# Used by:
# Modules from group: Entosis Link (6 of 6)
runtime = "late"
type = "passive"
def handler(fit, src, context):
    fit.extraAttributes['speedLimit'] = src.getModifiedItemAttr("speedLimit")
