# shipPDmgBonusMF
#
# Used by:
# Ship: Cheetah
# Ship: Freki
# Ship: Republic Fleet Firetail
# Ship: Rifter
# Ship: Slasher
# Ship: Stiletto
# Ship: Wolf
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
