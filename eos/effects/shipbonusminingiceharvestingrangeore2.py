# shipBonusMiningIceHarvestingRangeORE2
#
# Used by:
# Variations of ship: Covetor (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining") or mod.item.requiresSkill("Ice Harvesting"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusORE2") * level)
