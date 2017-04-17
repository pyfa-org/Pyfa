# ammoInfluenceCapNeed
#
# Used by:
# Items from category: Charge (466 of 913)
# Charges from group: Frequency Crystal (185 of 185)
# Charges from group: Hybrid Charge (209 of 209)
type = "passive"


def handler(fit, module, context):
    # Dirty hack to work around cap charges setting cap booster
    # injection amount to zero
    rawAttr = module.item.getAttribute("capacitorNeed")
    if rawAttr is not None and rawAttr >= 0:
        module.boostItemAttr("capacitorNeed", module.getModifiedChargeAttr("capNeedBonus") or 0)
