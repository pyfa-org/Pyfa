# Used by:
# Module: 'Smokescreen' Covert Ops Cloaking Device II
# Module: Covert Ops Cloaking Device II
type = "active"
runTime = "early"
def handler(fit, ship, context):
    fit.extraAttributes["cloaked"] = True
    #TODO: Implement