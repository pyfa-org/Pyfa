# Used by:
# Modules named like: Core Defense Purger (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Shield Implants > Implant Slot 09 (6 of 6)
# Implant: Sansha Modified 'Gnome' Implant
# Skill: Shield Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("shieldRechargeRate", container.getModifiedItemAttr("rechargeratebonus") * level)
