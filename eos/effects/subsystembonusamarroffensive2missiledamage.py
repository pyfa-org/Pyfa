# subsystemBonusAmarrOffensive2MissileDamage
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "explosiveDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2") * lvl, skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "kineticDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2") * lvl, skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "emDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2") * lvl, skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "thermalDamage", src.getModifiedItemAttr("subsystemBonusAmarrOffensive2") * lvl, skill="Amarr Offensive Systems")
