# subsystemBonusAmarrOffensive2MissileDamage
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                    "explosiveDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                    "emDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                    "thermalDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
