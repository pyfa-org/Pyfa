# Used by:
# Items from market group: Ship Equipment > Fleet Assistance Modules > Mining Foreman Links (6 of 6)
# Items from market group: Ship Equipment > Fleet Assistance Modules > Warfare Links (24 of 24)
type = "passive"
def handler(fit, module, context):
    module.increaseItemAttr("cpu", module.getModifiedItemAttr("warfareLinkCPUAdd") or 0)
