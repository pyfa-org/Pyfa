from functools import reduce

from eos.saveddata.damagePattern import DamagePattern

from gui.utils.numberFormatter import formatAmount


tankTypes = ("shield", "armor", "hull")
damageTypes = ("em", "thermal", "kinetic", "explosive")
damagePatterns = [DamagePattern.oneType(damageType) for damageType in damageTypes]
damageTypeResonanceNames = [damageType.capitalize() + "DamageResonance" for damageType in damageTypes]
resonanceNames = {"shield": ["shield" + s for s in damageTypeResonanceNames],
                  "armor": ["armor" + s for s in damageTypeResonanceNames],
                  "hull": [s[0].lower() + s[1:] for s in damageTypeResonanceNames]}


def firepowerSection(fit):
    """ Returns the text of the firepower section"""
    firepower = [fit.totalDPS, fit.weaponDPS, fit.droneDPS, fit.totalVolley]
    firepowerStr = [formatAmount(dps, 3, 0, 0) for dps in firepower]
    showWeaponAndDroneDps = (fit.weaponDPS > 0) and (fit.droneDPS > 0)
    if sum(firepower) == 0:
        return ""
    return "DPS: {} (".format(firepowerStr[0]) + \
           ("Weapon: {}, Drone: {}, ".format(*firepowerStr[1:3]) if showWeaponAndDroneDps else "") + \
           ("Volley: {})\n".format(firepowerStr[3]))


def tankSection(fit):
    """ Returns the text of the tank section"""
    ehp = [fit.ehp[tank] for tank in tankTypes] if fit.ehp is not None else [0, 0, 0]
    ehp.append(sum(ehp))
    ehpStr = [formatAmount(ehpVal, 3, 0, 9) for ehpVal in ehp]
    resists = {tankType: [1 - fit.ship.getModifiedItemAttr(s) for s in resonanceNames[tankType]] for tankType in tankTypes}
    ehpAgainstDamageType = [sum(pattern.calculateEhp(fit).values()) for pattern in damagePatterns]
    ehpAgainstDamageTypeStr = [formatAmount(ehpVal, 3, 0, 9) for ehpVal in ehpAgainstDamageType]

    return \
        "        {:>7} {:>7} {:>7} {:>7} {:>7}\n".format("TOTAL", "EM", "THERM", "KIN", "EXP") + \
        "EHP     {:>7} {:>7} {:>7} {:>7} {:>7}\n".format(ehpStr[3], *ehpAgainstDamageTypeStr) + \
        "Shield  {:>7} {:>7.0%} {:>7.0%} {:>7.0%} {:>7.0%}\n".format(ehpStr[0], *resists["shield"]) + \
        "Armor   {:>7} {:>7.0%} {:>7.0%} {:>7.0%} {:>7.0%}\n".format(ehpStr[1], *resists["armor"]) + \
        "Hull    {:>7} {:>7.0%} {:>7.0%} {:>7.0%} {:>7.0%}\n".format(ehpStr[2], *resists["hull"])


def repsSection(fit):
    """ Returns the text of the repairs section"""
    selfRep = [fit.effectiveTank[tankType + "Repair"] for tankType in tankTypes]
    sustainRep = [fit.effectiveSustainableTank[tankType + "Repair"] for tankType in tankTypes]
    remoteRep = [fit.remoteReps[tankType.capitalize()] for tankType in tankTypes]
    shieldRegen = [fit.effectiveSustainableTank["passiveShield"], 0, 0]
    shieldRechargeModuleMultipliers = [module.item.attributes["shieldRechargeRateMultiplier"].value for module in
                                       fit.modules if
                                       module.item and "shieldRechargeRateMultiplier" in module.item.attributes]
    shieldRechargeMultiplierByModules = reduce(lambda x, y: x * y, shieldRechargeModuleMultipliers, 1)
    if shieldRechargeMultiplierByModules >= 0.9:  # If the total affect of modules on the shield recharge is negative or insignificant, we don't care about it
        shieldRegen[0] = 0
    totalRep = list(zip(selfRep, remoteRep, shieldRegen))
    totalRep = list(map(sum, totalRep))

    selfRep.append(sum(selfRep))
    sustainRep.append(sum(sustainRep))
    remoteRep.append(sum(remoteRep))
    shieldRegen.append(sum(shieldRegen))
    totalRep.append(sum(totalRep))

    totalSelfRep = selfRep[-1]
    totalRemoteRep = remoteRep[-1]
    totalShieldRegen = shieldRegen[-1]

    text = ""

    if sum(totalRep) > 0:  # Most commonly, there are no reps at all; then we skip this section
        singleTypeRep = None
        singleTypeRepName = None
        if totalRemoteRep == 0 and totalShieldRegen == 0:  # Only self rep
            singleTypeRep = selfRep[:-1]
            singleTypeRepName = "Self"
        if totalSelfRep == 0 and totalShieldRegen == 0:  # Only remote rep
            singleTypeRep = remoteRep[:-1]
            singleTypeRepName = "Remote"
        if totalSelfRep == 0 and totalRemoteRep == 0:  # Only shield regen
            singleTypeRep = shieldRegen[:-1]
            singleTypeRepName = "Regen"
        if singleTypeRep and sum(
                x > 0 for x in singleTypeRep) == 1:  # Only one type of reps and only one tank type is repaired
            index = next(i for i, v in enumerate(singleTypeRep) if v > 0)
            if singleTypeRepName == "Regen":
                text += "Shield regeneration: {} EHP/s".format(formatAmount(singleTypeRep[index], 3, 0, 9))
            else:
                text += "{} {} repair: {} EHP/s".format(singleTypeRepName, tankTypes[index],
                                                        formatAmount(singleTypeRep[index], 3, 0, 9))
            if (singleTypeRepName == "Self") and (sustainRep[index] != singleTypeRep[index]):
                text += " (Sustained: {} EHP/s)".format(formatAmount(sustainRep[index], 3, 0, 9))
            text += "\n"
        else:  # Otherwise show a table
            selfRepStr = [formatAmount(rep, 3, 0, 9) for rep in selfRep]
            sustainRepStr = [formatAmount(rep, 3, 0, 9) for rep in sustainRep]
            remoteRepStr = [formatAmount(rep, 3, 0, 9) for rep in remoteRep]
            shieldRegenStr = [formatAmount(rep, 3, 0, 9) if rep != 0 else "" for rep in shieldRegen]
            totalRepStr = [formatAmount(rep, 3, 0, 9) for rep in totalRep]

            header = "REPS    "
            lines = [
                "Shield  ",
                "Armor   ",
                "Hull    ",
                "Total   "
            ]

            showSelfRepColumn = totalSelfRep > 0
            showSustainRepColumn = sustainRep != selfRep
            showRemoteRepColumn = totalRemoteRep > 0
            showShieldRegenColumn = totalShieldRegen > 0

            if showSelfRepColumn + showSustainRepColumn + showRemoteRepColumn + showShieldRegenColumn > 1:
                header += "{:>7} ".format("TOTAL")
                lines = [line + "{:>7} ".format(rep) for line, rep in zip(lines, totalRepStr)]
            if showSelfRepColumn:
                header += "{:>7} ".format("SELF")
                lines = [line + "{:>7} ".format(rep) for line, rep in zip(lines, selfRepStr)]
            if showSustainRepColumn:
                header += "{:>7} ".format("SUST")
                lines = [line + "{:>7} ".format(rep) for line, rep in zip(lines, sustainRepStr)]
            if showRemoteRepColumn:
                header += "{:>7} ".format("REMOTE")
                lines = [line + "{:>7} ".format(rep) for line, rep in zip(lines, remoteRepStr)]
            if showShieldRegenColumn:
                header += "{:>7} ".format("REGEN")
                lines = [line + "{:>7} ".format(rep) for line, rep in zip(lines, shieldRegenStr)]

            text += header + "\n"
            repsByTank = zip(totalRep, selfRep, sustainRep, remoteRep, shieldRegen)
            for line in lines:
                reps = next(repsByTank)
                if sum(reps) > 0:
                    text += line + "\n"
    return text


def miscSection(fit):
    text = ""
    text += "Speed: {} m/s\n".format(formatAmount(fit.maxSpeed, 3, 0, 0))
    text += "Signature: {} m\n".format(formatAmount(fit.ship.getModifiedItemAttr("signatureRadius"), 3, 0, 9))

    text += "Capacitor: {} GJ".format(formatAmount(fit.ship.getModifiedItemAttr("capacitorCapacity"), 3, 0, 9))
    capState = fit.capState
    if fit.capStable:
        text += " (Stable at {0:.0f}%)".format(capState)
    else:
        text += " (Lasts {})".format("%ds" % capState if capState <= 60 else "%dm%ds" % divmod(capState, 60))
    text += "\n"

    text += "Targeting range: {} km\n".format(formatAmount(fit.maxTargetRange / 1000, 3, 0, 0))
    text += "Scan resolution: {0:.0f} mm\n".format(fit.ship.getModifiedItemAttr("scanResolution"))
    text += "Sensor strength: {}\n".format(formatAmount(fit.scanStrength, 3, 0, 0))

    return text


def statsExportText(fit):
    """ Returns the text of the stats export of the given fit"""
    sections = filter(None, (firepowerSection(fit),  # Prune empty sections
                             tankSection(fit),
                             repsSection(fit),
                             miscSection(fit)))

    text = "{} ({})\n".format(fit.name, fit.ship.name) + "\n"
    text += "\n".join(sections)

    return text
