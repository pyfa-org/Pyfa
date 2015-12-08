# remoteArmorRepairFalloff
#
# Used by:
# Modules from group: Remote Armor Repairer (33 of 33)
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.getModifiedItemAttr("duration") / 1000.0
        fit.extraAttributes.increase("armorRepair", bonus / duration)
