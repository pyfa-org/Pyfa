# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"), "virusStrength", src.getModifiedItemAttr("virusStrengthBonus"))
