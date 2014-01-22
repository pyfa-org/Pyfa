# Used by:
# Charges from group: Advanced Pulse Laser Crystal (6 of 6)
# Charges from group: Advanced Railgun Charge (6 of 6)
# Charges from group: Capacitor Booster Charge (16 of 16)
# Charges from group: Frequency Crystal (185 of 185)
# Charges from group: Hybrid Charge (209 of 209)
# Charges from group: Mercoxit Mining Crystal (2 of 2)
# Charges from group: Mining Crystal (30 of 30)
# Charge: Focused Warp Disruption Script
# Charge: Void L
# Charge: Void M
# Charge: Void S
type = "passive"
def handler(fit, module, context):
    # Dirty hack to work around cap charges setting cap booster
    # injection amount to zero
    rawAttr = module.item.getAttribute("capacitorNeed")
    if rawAttr is not None and rawAttr >= 0:
        module.boostItemAttr("capacitorNeed", module.getModifiedChargeAttr("capNeedBonus") or 0)
