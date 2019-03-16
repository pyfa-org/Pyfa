# hackingVirusStrengthBonus
#
# Used by:
# Implant: Neural Lace 'Blackglass' Net Intrusion 920-40
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Hacking"), "virusStrength", src.getModifiedItemAttr("virusStrengthBonus"))
