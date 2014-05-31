# Used by:
# Implants named like: Low grade Slave (10 of 12)
# Implants named like: Low grade Snake Epsilon (2 of 2)
# Implants named like: Slave (15 of 18)
# Modules named like: Trimark Armor Pump (8 of 8)
# Skill: Hull Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("armorHP", (container.getModifiedItemAttr("armorHpBonus") or 0) * level)
