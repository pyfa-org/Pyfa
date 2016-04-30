# targetArmorRepair
#
# Used by:
# Module: QA Remote Armor Repair System - 5 Players
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("armorRepair", bonus / duration)
