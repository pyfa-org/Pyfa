# shipModuleRemoteShieldBooster
#
# Used by:
# Modules from group: Remote Shield Booster (38 of 38)
type = "projected", "active"


def handler(fit, container, context, **kwargs):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("shieldBonus")
        duration = container.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("shieldRepair", bonus / duration, **kwargs)
