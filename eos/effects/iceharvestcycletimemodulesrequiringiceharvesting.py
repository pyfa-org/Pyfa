# Used by:
# Implant: Inherent Implants 'Yeti' Ice Harvesting IH-1001
# Implant: Inherent Implants 'Yeti' Ice Harvesting IH-1003
# Implant: Inherent Implants 'Yeti' Ice Harvesting IH-1005
# Module: Medium Ice Harvester Accelerator I
# Skill: Ice Harvesting
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "duration", container.getModifiedItemAttr("iceHarvestCycleBonus") * level)
