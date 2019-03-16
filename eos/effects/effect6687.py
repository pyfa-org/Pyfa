# npcEntityRemoteArmorRepairer
#
# Used by:
# Drones named like: Armor Maintenance Bot (6 of 6)
type = "projected", "active"


def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.getModifiedItemAttr("duration") / 1000.0
        rps = bonus / duration
        fit.extraAttributes.increase("armorRepair", rps)
        fit.extraAttributes.increase("armorRepairPreSpool", rps)
        fit.extraAttributes.increase("armorRepairFullSpool", rps)
