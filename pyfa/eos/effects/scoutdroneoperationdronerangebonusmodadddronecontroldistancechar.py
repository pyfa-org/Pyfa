# scoutDroneOperationDroneRangeBonusModAddDroneControlDistanceChar
#
# Used by:
# Modules named like: Drone Control Range Augmentor (8 of 8)
# Skills named like: Drone Avionics (2 of 2)
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    amount = container.getModifiedItemAttr("droneRangeBonus") * level
    fit.extraAttributes.increase("droneControlRange", amount)
