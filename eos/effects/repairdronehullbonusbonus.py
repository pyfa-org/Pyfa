# Used by:
# Modules named like: Drone Repair Augmentor (8 of 8)
# Skill: Repair Drone Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                 "structureDamageAmount", container.getModifiedItemAttr("damageHP") * level)
