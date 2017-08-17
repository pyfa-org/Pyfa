# useMissiles
#
# Used by:
# Modules from group: Missile Launcher Heavy (12 of 12)
# Modules from group: Missile Launcher Rocket (15 of 15)
# Modules named like: Launcher (154 of 154)
type = 'active', "projected"


def handler(fit, src, context):
    # Set reload time to 10 seconds
    src.reloadTime = 10000

    if "projected" in context:
        if src.item.group.name == 'Missile Launcher Bomb':
            # Bomb Launcher Cooldown Timer
            moduleReactivationDelay = src.getModifiedItemAttr("moduleReactivationDelay")

            # Void and Focused Void Bombs
            neutAmount = src.getModifiedChargeAttr("energyNeutralizerAmount")

            if moduleReactivationDelay and neutAmount:
                fit.addDrain(src, moduleReactivationDelay, neutAmount, 0)

            # Lockbreaker Bombs
            ecmStrengthBonus = src.getModifiedChargeAttr("scan{0}StrengthBonus".format(fit.scanType))

            if ecmStrengthBonus:
                strModifier = 1 - ecmStrengthBonus / fit.scanStrength
                fit.ecmProjectedStr *= strModifier
