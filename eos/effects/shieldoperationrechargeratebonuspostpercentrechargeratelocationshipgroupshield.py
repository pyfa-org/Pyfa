# Used by:
# Implants named like: Zainou 'Gnome' Shield Operation SP (6 of 6)
# Modules named like: Core Defense Field Purger (8 of 8)
# Implant: Sansha Modified 'Gnome' Implant
# Skill: Shield Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("shieldRechargeRate", container.getModifiedItemAttr("rechargeratebonus") * level)
