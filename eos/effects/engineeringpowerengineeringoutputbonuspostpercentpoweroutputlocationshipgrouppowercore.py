# Used by:
# Implants named like: Inherent Implants 'Squire' Engineering EG (6 of 6)
# Modules named like: Ancillary Current Router (8 of 8)
# Implant: Genolution Core Augmentation CA-1
# Skill: Power Grid Management
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("powerOutput", container.getModifiedItemAttr("powerEngineeringOutputBonus") * level)
