# shipBonusSupercarrierC2AfterburnerBonus
#
# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedFactor", src.getModifiedItemAttr("shipBonusSupercarrierC2"), skill="Caldari Carrier")
