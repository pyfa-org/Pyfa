# ammoInfluenceCapNeed
#
# Used by:
# Items from category: Charge (464 of 898)
# Charges from group: Frequency Crystal (184 of 184)
# Charges from group: Hybrid Charge (208 of 208)
type = "passive"


def handler(fit, module, context):
    # Dirty hack to work around cap charges setting cap booster
    # injection amount to zero
    rawAttr = module.item.getAttribute("capacitorNeed")
    if rawAttr is not None and rawAttr >= 0:
        module.boostItemAttr("capacitorNeed", module.getModifiedChargeAttr("capNeedBonus") or 0)
