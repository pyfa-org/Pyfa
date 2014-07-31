# Used by:
# Modules named like: Covert Ops Cloaking Device II (2 of 2)
type = "active"
runTime = "early"
def handler(fit, ship, context):
    fit.extraAttributes["cloaked"] = True
    #TODO: Implement