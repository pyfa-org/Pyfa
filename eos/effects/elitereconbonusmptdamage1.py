# eliteReconBonusMPTdamage1
#
# Used by:
# Ship: Huginn
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusReconShip1") * level)
