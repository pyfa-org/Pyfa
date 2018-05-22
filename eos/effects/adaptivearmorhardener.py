# adaptiveArmorHardener
#
# Used by:
# Module: Reactive Armor Hardener
from logbook import Logger
import eos.config

pyfalog = Logger(__name__)

runTime = "late"
type = "active"


def handler(fit, module, context):
    damagePattern = fit.damagePattern
    # pyfalog.debug("==============================")

    static_adaptive_behavior = eos.config.settings['useStaticAdaptiveArmorHardener']

    if (damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount) and static_adaptive_behavior:
        # pyfalog.debug("Setting adaptivearmorhardener resists to uniform profile.")
        for attr in ("armorEmDamageResonance", "armorThermalDamageResonance", "armorKineticDamageResonance", "armorExplosiveDamageResonance"):
            fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup="preMul")
        return

    # Skip if there is no damage pattern. Example: projected ships or fleet boosters
    if damagePattern:

        # Populate a tuple with the damage profile modified by current armor resists.
        baseDamageTaken = (
            damagePattern.emAmount * fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
            damagePattern.thermalAmount * fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
            damagePattern.kineticAmount * fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
            damagePattern.explosiveAmount * fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
        )
        # pyfalog.debug("Damage Adjusted for Armor Resists: %f/%f/%f/%f" % (baseDamageTaken[0], baseDamageTaken[1], baseDamageTaken[2], baseDamageTaken[3]))

        resistanceShiftAmount = module.getModifiedItemAttr(
            'resistanceShiftAmount') / 100  # The attribute is in percent and we want a fraction
        RAHResistance = [
            module.getModifiedItemAttr('armorEmDamageResonance'),
            module.getModifiedItemAttr('armorThermalDamageResonance'),
            module.getModifiedItemAttr('armorKineticDamageResonance'),
            module.getModifiedItemAttr('armorExplosiveDamageResonance'),
        ]

        # Simulate RAH cycles until the RAH either stops changing or enters a loop.
        # The number of iterations is limited to prevent an infinite loop if something goes wrong.
        cycleList = []
        loopStart = -20
        for num in range(50):
            # pyfalog.debug("Starting cycle %d." % num)
            # The strange order is to emulate the ingame sorting when different types have taken the same amount of damage.
            # This doesn't take into account stacking penalties. In a few cases fitting a Damage Control causes an inaccurate result.
            damagePattern_tuples = [
                (0, baseDamageTaken[0] * RAHResistance[0], RAHResistance[0]),
                (3, baseDamageTaken[3] * RAHResistance[3], RAHResistance[3]),
                (2, baseDamageTaken[2] * RAHResistance[2], RAHResistance[2]),
                (1, baseDamageTaken[1] * RAHResistance[1], RAHResistance[1]),
            ]

            # Sort the tuple to drop the highest damage value to the bottom
            sortedDamagePattern_tuples = sorted(damagePattern_tuples, key=lambda damagePattern: damagePattern[1])

            if sortedDamagePattern_tuples[2][1] == 0:
                # One damage type: the top damage type takes from the other three
                # Since the resistances not taking damage will end up going to the type taking damage we just do the whole thing at once.
                change0 = 1 - sortedDamagePattern_tuples[0][2]
                change1 = 1 - sortedDamagePattern_tuples[1][2]
                change2 = 1 - sortedDamagePattern_tuples[2][2]
                change3 = -(change0 + change1 + change2)
            elif sortedDamagePattern_tuples[1][1] == 0:
                # Two damage types: the top two damage types take from the other two
                # Since the resistances not taking damage will end up going equally to the types taking damage we just do the whole thing at once.
                change0 = 1 - sortedDamagePattern_tuples[0][2]
                change1 = 1 - sortedDamagePattern_tuples[1][2]
                change2 = -(change0 + change1) / 2
                change3 = -(change0 + change1) / 2
            else:
                # Three or four damage types: the top two damage types take from the other two
                change0 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[0][2])
                change1 = min(resistanceShiftAmount, 1 - sortedDamagePattern_tuples[1][2])
                change2 = -(change0 + change1) / 2
                change3 = -(change0 + change1) / 2

            RAHResistance[sortedDamagePattern_tuples[0][0]] = sortedDamagePattern_tuples[0][2] + change0
            RAHResistance[sortedDamagePattern_tuples[1][0]] = sortedDamagePattern_tuples[1][2] + change1
            RAHResistance[sortedDamagePattern_tuples[2][0]] = sortedDamagePattern_tuples[2][2] + change2
            RAHResistance[sortedDamagePattern_tuples[3][0]] = sortedDamagePattern_tuples[3][2] + change3
            # pyfalog.debug("Resistances shifted to %f/%f/%f/%f" % ( RAHResistance[0], RAHResistance[1], RAHResistance[2], RAHResistance[3]))

            # See if the current RAH profile has been encountered before, indicating a loop.
            for i, val in enumerate(cycleList):
                tolerance = 1e-06
                if abs(RAHResistance[0] - val[0]) <= tolerance and \
                            abs(RAHResistance[1] - val[1]) <= tolerance and \
                            abs(RAHResistance[2] - val[2]) <= tolerance and \
                            abs(RAHResistance[3] - val[3]) <= tolerance:
                    loopStart = i
                    # pyfalog.debug("Loop found: %d-%d" % (loopStart, num))
                    break
            if loopStart >= 0:
                break

            cycleList.append(list(RAHResistance))

        # if loopStart < 0:
            # pyfalog.error("Reactive Armor Hardener failed to find equilibrium. Damage profile after armor: {0}/{1}/{2}/{3}".format(
            #             baseDamageTaken[0], baseDamageTaken[1], baseDamageTaken[2], baseDamageTaken[3]))

        # Average the profiles in the RAH loop, or the last 20 if it didn't find a loop.
        loopCycles = cycleList[loopStart:]
        numCycles = len(loopCycles)
        average = [0, 0, 0, 0]
        for cycle in loopCycles:
            for i in range(4):
                average[i] += cycle[i]

        for i in range(4):
            average[i] = round(average[i] / numCycles, 3)

        # Set the new resistances
        # pyfalog.debug("Setting new resist profile: %f/%f/%f/%f" % ( average[0], average[1], average[2],average[3]))
        for i, attr in enumerate((
                'armorEmDamageResonance', 'armorThermalDamageResonance', 'armorKineticDamageResonance',
                'armorExplosiveDamageResonance')):
            module.increaseItemAttr(attr, average[i] - module.getModifiedItemAttr(attr))
            fit.ship.multiplyItemAttr(attr, average[i], stackingPenalties=True, penaltyGroup="preMul")
