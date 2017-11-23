# subsystemBonusMinmatarDefensiveShieldArmorHP
#
# Used by:
# Subsystem: Loki Defensive - Augmented Durability
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                           skill="Minmatar Defensive Systems")
    fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                           skill="Minmatar Defensive Systems")
