# shipBonusCarrierC4WarfareLinksBonus
#
# Used by:
# Ship: Chimera
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
        "warfareBuff2Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
        "buffDuration", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
        "warfareBuff3Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
        "warfareBuff4Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"),
        "warfareBuff1Value", src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
