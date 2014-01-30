# Used by:
# Implants named like: Implants 'Squire' Energy Systems Operation (6 of 6)
# Modules named like: Capacitor Circuit (8 of 8)
# Implant: Genolution Core Augmentation CA-2
# Skill: Capacitor Systems Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("rechargeRate", container.getModifiedItemAttr("capRechargeBonus") * level)
