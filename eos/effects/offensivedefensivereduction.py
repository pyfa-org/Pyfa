# Used by:
# Celestials named like: Incursion ship attributes effects (3 of 3)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    damages = ("em", "thermal", "kinetic", "explosive")
    for damage in damages:
        # Nerf missile damage
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        "{0}Damage".format(damage), beacon.getModifiedItemAttr("systemEffectDamageReduction"))
        # Nerf smartbomb damage
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Smart Bomb",
                                      "{0}Damage".format(damage), beacon.getModifiedItemAttr("systemEffectDamageReduction"))
        # Nerf armor resistances
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damage.capitalize()),
                               beacon.getModifiedItemAttr("armor{0}DamageResistanceBonus".format(damage.capitalize())))
        # Nerf shield resistances
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(damage.capitalize()),
                               beacon.getModifiedItemAttr("shield{0}DamageResistanceBonus".format(damage.capitalize())))
    # Nerf drone damage output
    fit.drones.filteredItemBoost(lambda drone: True,
                                 "damageMultiplier", beacon.getModifiedItemAttr("systemEffectDamageReduction"))
    # Nerf turret damage output
    fit.modules.filteredItemBoost(lambda module: module.item.requiresSkill("Gunnery"),
                                  "damageMultiplier", beacon.getModifiedItemAttr("systemEffectDamageReduction"))
