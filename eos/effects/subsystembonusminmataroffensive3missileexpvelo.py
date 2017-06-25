# subsystemBonusMinmatarOffensive3MissileExpVelo
#
# Used by:
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "aoeVelocity", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"), skill="Minmatar Offensive Systems")
