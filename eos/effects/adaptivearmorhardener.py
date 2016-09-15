# adaptiveArmorHardener
#
# Used by:
# Module: Reactive Armor Hardener
import logging
import operator

logger = logging.getLogger(__name__)

runTime = "late"
type = "active"
def handler(fit, module, context):
    damagePattern = fit.damagePattern

    # Skip if there is no damage pattern. Example: projected ships or fleet boosters
    if damagePattern:

        # Populate a tuple with the damage profile modified by current armor resists.
        # Build this up front as there are a number of values we only need to touch once
        damagePattern_tuple = []

        '''
        # Bit of documentation for how the tuple is layed out
        damagePattern_tuple.append(['RESIST TYPE',
                SHIP ARMOR RESIST AMOUNT,
                DAMAGE PATTERN AMOUNT,
                MODIFIED DAMAGE PATTERN AMOUNT (SHIP ARMOR RESIST AMOUNT * DAMAGE PATTERN AMOUND),
                ADAPTIVE RESIST AMOUNT,
                ADAPTIVE RESIST AMOUNT (Original))
        '''

        damagePattern_tuple.append(['Em',
                fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                damagePattern.emAmount,
                damagePattern.emAmount*fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                module.getModifiedItemAttr('armorEmDamageResonance'),
                module.getModifiedItemAttr('armorEmDamageResonance')])

        damagePattern_tuple.append(['Thermal',
                fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                damagePattern.thermalAmount,
                damagePattern.thermalAmount * fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                module.getModifiedItemAttr('armorThermalDamageResonance'),
                module.getModifiedItemAttr('armorThermalDamageResonance')])

        damagePattern_tuple.append(['Kinetic',
                fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                damagePattern.kineticAmount,
                damagePattern.kineticAmount*fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                module.getModifiedItemAttr('armorKineticDamageResonance'),
                module.getModifiedItemAttr('armorKineticDamageResonance')])

        damagePattern_tuple.append(['Explosive',
                fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
                damagePattern.explosiveAmount,
                damagePattern.explosiveAmount*fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
                module.getModifiedItemAttr('armorExplosiveDamageResonance'),
                module.getModifiedItemAttr('armorExplosiveDamageResonance')])

        runLoop = 1
        countPasses = 0
        resistanceShiftAmount = module.getModifiedItemAttr('resistanceShiftAmount')/100
        while runLoop == 1:

            for i in range(4):
                # Update tuple with current values
                attr = "armor%sDamageResonance" % damagePattern_tuple[i][0].capitalize()
                damagePattern_tuple[i][3] = damagePattern_tuple[i][2] * damagePattern_tuple[i][1]
                damagePattern_tuple[i][4] = module.getModifiedItemAttr(attr)
                #logger.debug("Update values (Type|Resist|ModifiedDamage|AdaptiveResists): %s | %f | %f | %f", damagePattern_tuple[i][0], fit.ship.getModifiedItemAttr(attr), damagePattern_tuple[i][3], damagePattern_tuple[i][4])

            # Sort the tuple by which resist took the most damage
            damagePattern_tuple = sorted(damagePattern_tuple, key=operator.itemgetter(3,0))

            if damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount:
                # If damage pattern is even across the board, we "reset" back to default resists.
                logger.debug("Setting adaptivearmorhardener resists to uniform profile.")
                damagePattern_tuple[0][4]=damagePattern_tuple[0][5]
                damagePattern_tuple[1][4]=damagePattern_tuple[0][5]
                damagePattern_tuple[2][4]=damagePattern_tuple[0][5]
                damagePattern_tuple[3][4]=damagePattern_tuple[0][5]
                runLoop = 0
            elif damagePattern_tuple[2][2] == 0:
                # If damage pattern is a single source, we set all resists to one damage profile.
                logger.debug("Setting adaptivearmorhardener resists to single damage profile.")
                damagePattern_tuple[0][4]=1
                damagePattern_tuple[1][4]=1
                damagePattern_tuple[2][4]=1
                damagePattern_tuple[3][4]=.4
                runLoop = 0
            else:
                # We have more than one damage source
                if damagePattern_tuple[1][4] == 1 == damagePattern_tuple[0][4]:
                    logger.debug("We've run out of resists to steal. Breaking out of RAH cycle.")
                    break
                elif damagePattern_tuple[0][4] == 1:
                    # If our weakest resist is at 0, and we're still looping, bail out after we've tried this a few times.
                    # Most likely the RAH is cycling between two different profiles and is in an infinite loop.
                    countPasses = countPasses+1

                    # Reduce the amount of resists we shift each loop, to try and stabilize on a more average profile.
                    if resistanceShiftAmount > .01:
                        resistanceShiftAmount = resistanceShiftAmount - .01
                        logger.debug("Reducing resistance shift amount to %f", resistanceShiftAmount)

                    if countPasses == 15:
                        logger.debug("Looped %f times. Most likely the RAH is cycling between two different profiles and is in an infinite loop. Breaking out of RAH cycle.", countPasses)
                        break
                    else:
                        pass

                # Loop through the resists that did least damage and figure out how much there is to steal
                vampDmg=[0]*2
                for i in [0,1]:
                    attr = "armor%sDamageResonance" % damagePattern_tuple[i][0].capitalize()
                    if damagePattern_tuple[i][4] < 1-resistanceShiftAmount:
                        # If there is more than 3% to steal, let's steal 3% and reduce the resit by that amount.
                        vampDmg[i] = resistanceShiftAmount
                    else:
                        # If there is equal to or less than 3% left to steal, grab what we can and set the resist to 0%.
                        vampDmg[i] = 1-damagePattern_tuple[i][4]

                    # Adjust the module resists down
                    if vampDmg[i] > 0:
                        module.increaseItemAttr(attr, vampDmg[i])
                        # Set our "ship" resists
                        damagePattern_tuple[i][1] = fit.ship.getModifiedItemAttr(attr) * module.getModifiedItemAttr(attr)

                #Add up the two amounts we stole, and divide it equally between the two
                vampDmgTotal = vampDmg[0] + vampDmg[1]

                # Loop through the resists that took the most damage, and add what we vamped from the weakest resists.
                for i in [2,3]:
                    attr = "armor%sDamageResonance" % damagePattern_tuple[i][0].capitalize()
                    # And by add we mean subtract, because in CCPland up is down and down is up
                    if vampDmgTotal > 0:
                        module.increaseItemAttr(attr, 0-(vampDmgTotal/2))
                        # Set our "ship" resists
                        damagePattern_tuple[i][1] = fit.ship.getModifiedItemAttr(attr)*module.getModifiedItemAttr(attr)

            adaptiveResists_tuple = [0.0] * 12
            for damagePatternType in damagePattern_tuple:
                attr = "armor%sDamageResonance" % damagePatternType[0].capitalize()

                if damagePatternType[0] == 'Em':
                    adaptiveResists_tuple[0] = module.getModifiedItemAttr(attr)
                    adaptiveResists_tuple[4] = damagePatternType[1]
                    adaptiveResists_tuple[8] = damagePatternType[3]
                elif damagePatternType[0] == 'Thermal':
                    adaptiveResists_tuple[1] = module.getModifiedItemAttr(attr)
                    adaptiveResists_tuple[5] = damagePatternType[1]
                    adaptiveResists_tuple[9] = damagePatternType[3]
                elif damagePatternType[0] == 'Kinetic':
                    adaptiveResists_tuple[2] = module.getModifiedItemAttr(attr)
                    adaptiveResists_tuple[6] = damagePatternType[1]
                    adaptiveResists_tuple[10] = damagePatternType[3]
                elif damagePatternType[0] == 'Explosive':
                    adaptiveResists_tuple[3] = module.getModifiedItemAttr(attr)
                    adaptiveResists_tuple[7] = damagePatternType[1]
                    adaptiveResists_tuple[11] = damagePatternType[3]

            logger.debug(
                "Adaptive Resists, Ship Resists, Modified Damage (EM|The|Kin|Exp) : %f | %f | %f | %f || %f | %f | %f | %f || %f | %f | %f | %f",
                adaptiveResists_tuple[0], adaptiveResists_tuple[1], adaptiveResists_tuple[2], adaptiveResists_tuple[3],
                adaptiveResists_tuple[4], adaptiveResists_tuple[5], adaptiveResists_tuple[6], adaptiveResists_tuple[7],
                adaptiveResists_tuple[8], adaptiveResists_tuple[9], adaptiveResists_tuple[10],
                adaptiveResists_tuple[11])

        adaptiveResists_tuple = [0.0] * 12
        # Apply module resists to the ship (for reals this time and not just pretend)
        for damagePatternType in damagePattern_tuple:
            attr = "armor%sDamageResonance" % damagePatternType[0].capitalize()

            fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup="preMul")

            if damagePatternType[0] == 'Em':
                adaptiveResists_tuple[0] = module.getModifiedItemAttr(attr)
                adaptiveResists_tuple[4] = fit.ship.getModifiedItemAttr(attr)
                adaptiveResists_tuple[8] = damagePatternType[3]
            elif damagePatternType[0] == 'Thermal':
                adaptiveResists_tuple[1] = module.getModifiedItemAttr(attr)
                adaptiveResists_tuple[5] = fit.ship.getModifiedItemAttr(attr)
                adaptiveResists_tuple[9] = damagePatternType[3]
            elif damagePatternType[0] == 'Kinetic':
                adaptiveResists_tuple[2] = module.getModifiedItemAttr(attr)
                adaptiveResists_tuple[6] = fit.ship.getModifiedItemAttr(attr)
                adaptiveResists_tuple[10] = damagePatternType[3]
            elif damagePatternType[0] == 'Explosive':
                adaptiveResists_tuple[3] = module.getModifiedItemAttr(attr)
                adaptiveResists_tuple[7] = fit.ship.getModifiedItemAttr(attr)
                adaptiveResists_tuple[11] = damagePatternType[3]

        logger.debug(
            "Adaptive Resists, Ship Resists, Modified Damage (EM|The|Kin|Exp) : %f | %f | %f | %f || %f | %f | %f | %f || %f | %f | %f | %f",
            adaptiveResists_tuple[0], adaptiveResists_tuple[1], adaptiveResists_tuple[2], adaptiveResists_tuple[3],
            adaptiveResists_tuple[4], adaptiveResists_tuple[5], adaptiveResists_tuple[6], adaptiveResists_tuple[7],
            adaptiveResists_tuple[8], adaptiveResists_tuple[9], adaptiveResists_tuple[10], adaptiveResists_tuple[11])
