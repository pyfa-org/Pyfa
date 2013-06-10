# Used by:
# Variations of module: Information Warfare Link - Recon Operation I (2 of 2)
type = "gang", "active"
gangBoost = "electronicMaxRange"
def handler(fit, module, context):
    if "gang" not in context: return
    groups = ("Target Painter", "Tracking Disruptor", "Remote Sensor Damper", "ECM", "ECM Burst")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "maxRange", module.getModifiedItemAttr("commandBonus"),
                                  stackingPenalties = True)
