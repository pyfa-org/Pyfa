# structureArmorHPBonus
#
# Used by:
# Structure Modules from group: Structure Armor Reinforcer (2 of 2)
type = "passive"
runTime = "early"


def handler(fit, src, context):
    fit.ship.boostItemAttr("hiddenArmorHPMultiplier", src.getModifiedItemAttr("armorHpBonus"), stackingPenalties=True)
