# Used by:
# Implant: Zor's Custom Navigation Hyper-Link
# Skill: Acceleration Control
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "speedFactor", container.getModifiedItemAttr("speedFBonus") * level)
