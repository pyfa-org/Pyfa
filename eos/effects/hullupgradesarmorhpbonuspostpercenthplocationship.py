# Used by:
# Implants named like: Slave (10 of 12)
# Modules named like: Trimark Armor Pump (8 of 8)
# Implant: Low-grade Snake Epsilon
# Skill: Hull Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("armorHP", (container.getModifiedItemAttr("armorHpBonus") or 0) * level)
