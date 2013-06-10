# Used by:
# Implants named like: Inherent Implants 'Noble' Hull Upgrades HG (7 of 7)
# Implant: Imperial Navy Modified 'Noble' Implant
# Implant: Imperial Special Ops Field Enhancer - Standard
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("armorHP", implant.getModifiedItemAttr("armorHpBonus2"))