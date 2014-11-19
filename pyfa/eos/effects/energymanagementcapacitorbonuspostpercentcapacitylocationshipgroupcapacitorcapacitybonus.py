# energyManagementCapacitorBonusPostPercentCapacityLocationShipGroupCapacitorCapacityBonus
#
# Used by:
# Implants named like: Inherent Implants 'Squire' Capacitor Management EM (6 of 6)
# Implants named like: Mindflood Booster (4 of 4)
# Modules named like: Semiconductor Memory Cell (8 of 8)
# Implant: Genolution Core Augmentation CA-1
# Skill: Capacitor Management
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("capacitorCapacity", container.getModifiedItemAttr("capacitorCapacityBonus") * level)
