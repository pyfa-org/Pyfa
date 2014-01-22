# Used by:
# Modules named like: Field Extender (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Shield Implants > Implant Slot 07 (7 of 7)
# Implant: Genolution Core Augmentation CA-3
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
# Skill: Shield Management
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("shieldCapacity", container.getModifiedItemAttr("shieldCapacityBonus") * level)
