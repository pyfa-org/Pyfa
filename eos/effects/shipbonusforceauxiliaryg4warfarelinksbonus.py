# shipBonusForceAuxiliaryG4WarfareLinksBonus
#
# Used by:
# Ship: Ninazu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
        "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
        "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
        "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
        "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
        "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
