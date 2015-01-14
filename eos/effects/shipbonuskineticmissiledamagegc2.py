# shipBonusKineticMissileDamageGC2
#
# Used by:
# Ship: Chameleon
# Ship: Gila
# Ship: 毒蜥级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusGC2") * level)
