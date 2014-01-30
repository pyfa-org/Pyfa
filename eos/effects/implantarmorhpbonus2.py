# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Armor Implants > Implant Slot 10 (8 of 8)
# Implant: Genolution Core Augmentation CA-4
# Implant: Imperial Special Ops Field Enhancer - Standard
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("armorHP", implant.getModifiedItemAttr("armorHpBonus2"))