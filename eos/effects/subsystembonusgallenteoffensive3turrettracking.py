# subsystemBonusGallenteOffensive3TurretTracking
#
# Used by:
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", module.getModifiedItemAttr("subsystemBonusGallenteOffensive3"),
                                  skill="Gallente Offensive Systems")
