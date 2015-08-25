runtime = "late"
type = "passive"
def handler(fit, src, context):
    fit.extraAttributes['speedLimit'] = src.getModifiedItemAttr("speedLimit")
