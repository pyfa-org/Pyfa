# Used by:
# Modules named like: Armor Pump (8 of 8)
# Implant: Low-grade Slave Alpha
# Implant: Low-grade Slave Beta
# Implant: Low-grade Slave Delta
# Implant: Low-grade Slave Epsilon
# Implant: Low-grade Slave Gamma
# Implant: Low-grade Snake Epsilon
# Implant: Slave Alpha
# Implant: Slave Beta
# Implant: Slave Delta
# Implant: Slave Epsilon
# Implant: Slave Gamma
# Skill: Hull Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("armorHP", (container.getModifiedItemAttr("armorHpBonus") or 0) * level)
