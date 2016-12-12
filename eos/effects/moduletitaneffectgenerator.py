# moduleTitanEffectGenerator
#
# Used by:
# Modules from group: Titan Phenomena Generator (4 of 4)

type = "active", "gang"
def handler(fit, module, context, **kwargs):
    def runEffect(id, value):
        if id == 39:  # Avatar Effect Generator : Capacitor Recharge bonus
            fit.ship.boostItemAttr("rechargeRate", value, stackingPenalties=True)

        if id == 40:  # Avatar Effect Generator : Kinetic resistance bonus
            for attr in ("armorKineticDamageResonance", "shieldKineticDamageResonance", "hullKineticDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 49:  # Avatar Effect Generator : EM resistance penalty
            for attr in ("armorEmDamageResonance", "shieldEmDamageResonance", "hullEmDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 42:  # Erebus Effect Generator : Armor HP bonus
            fit.ship.boostItemAttr("armorHP", value, stackingPenalties=True)

        if id == 43:  # Erebus Effect Generator : Explosive resistance bonus
            for attr in ("armorExplosiveDamageResonance", "shieldExplosiveDamageResonance", "hullExplosiveDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 44:  # Erebus Effect Generator : Thermal resistance penalty
            for attr in ("armorThermalDamageResonance", "shieldThermalDamageResonance", "hullThermalDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 45:  # Ragnarok Effect Generator : Signature Radius bonus
            fit.ship.boostItemAttr("signatureRadius", value, stackingPenalties=True)

        if id == 46:  # Ragnarok Effect Generator : Thermal resistance bonus
            for attr in ("armorThermalDamageResonance", "shieldThermalDamageResonance", "hullThermalDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 47:  # Ragnarok Effect Generator : Explosive resistance penaly
            for attr in ("armorExplosiveDamageResonance", "shieldExplosiveDamageResonance", "hullExplosiveDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 48:  # Leviathan Effect Generator : Shield HP bonus
            fit.ship.boostItemAttr("shieldCapacity", value, stackingPenalties=True)

        if id == 49:  # Leviathan Effect Generator : EM resistance bonus
            for attr in ("armorEmDamageResonance", "shieldEmDamageResonance", "hullEmDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 50:  # Leviathan Effect Generator : Kinetic resistance penalty
            for attr in ("armorKineticDamageResonance", "shieldKineticDamageResonance", "hullKineticDamageResonance"):
                fit.ship.boostItemAttr(attr, value)

        if id == 51:  # Avatar Effect Generator : Velocity penalty
            fit.ship.boostItemAttr("maxVelocity", value, stackingPenalties=True)

        if id == 52:  # Erebus Effect Generator : Shield RR penalty
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "shieldBonus", value, stackingPenalties=True)

        if id == 53:  # Leviathan Effect Generator : Armor RR penalty
            fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "armorDamageAmount", value, stackingPenalties=True)

        if id == 54:  # Ragnarok Effect Generator : Laser and Hybrid Optimal penalty
            groups = ("Energy Weapon", "Hybrid Weapon")
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups, "maxRange", value, stackingPenalties=True)

    for x in xrange(1, 4):
        if module.getModifiedItemAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedItemAttr("warfareBuff{}ID".format(x))

            if id:
                if 'commandRun' not in context:
                    fit.addCommandBonus(id, value, module, kwargs['effect'])
                elif kwargs['warfareBuffID'] is not None and kwargs['warfareBuffID'] == id:
                    runEffect(kwargs['warfareBuffID'], value)

