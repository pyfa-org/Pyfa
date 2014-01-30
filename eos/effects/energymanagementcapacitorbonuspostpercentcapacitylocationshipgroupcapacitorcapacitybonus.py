# Used by:
# Modules named like: Semiconductor Cell (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Engineering Implants > Implant Slot 08 (6 of 6)
# Implant: Genolution Core Augmentation CA-1
# Implant: Improved Mindflood Booster
# Implant: Standard Mindflood Booster
# Implant: Strong Mindflood Booster
# Implant: Synth Mindflood Booster
# Skill: Capacitor Management
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("capacitorCapacity", container.getModifiedItemAttr("capacitorCapacityBonus") * level)
