# adaptiveArmorHardener
#
# Used by:
# Module: Reactive Armor Hardener
import logging

logger = logging.getLogger(__name__)

runTime = "late"
type = "active"
def handler(fit, module, context):
    damagePattern = fit.damagePattern

    # Skip if there is no damage pattern. Example: projected ships or fleet boosters
    if damagePattern:

        # Populate a tuple with the damage profile modified by current armor resists.

        damagePattern_tuple = []

        damagePattern_tuple.append(['Em',
                fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                damagePattern.emAmount,
                damagePattern.emAmount*fit.ship.getModifiedItemAttr('armorEmDamageResonance'),
                module.getModifiedItemAttr('armorEmDamageResonance')])

        damagePattern_tuple.append(['Thermal',
                fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                damagePattern.thermalAmount,
                damagePattern.thermalAmount * fit.ship.getModifiedItemAttr('armorThermalDamageResonance'),
                module.getModifiedItemAttr('armorThermalDamageResonance')])

        damagePattern_tuple.append(['Kinetic',
                fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                damagePattern.kineticAmount,
                damagePattern.kineticAmount*fit.ship.getModifiedItemAttr('armorKineticDamageResonance'),
                module.getModifiedItemAttr('armorKineticDamageResonance')])

        damagePattern_tuple.append(['Explosive',
                fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
                damagePattern.explosiveAmount,
                damagePattern.explosiveAmount*fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'),
                module.getModifiedItemAttr('armorExplosiveDamageResonance')])

        runLoop = 1
        countPasses = 0
        while runLoop == 1:

            # Update tuple with current values
            # damagePattern_tuple[0]
            attr = "armor%sDamageResonance" % damagePattern_tuple[0][0].capitalize()
            damagePattern_tuple[0][1] = fit.ship.getModifiedItemAttr(attr)
            damagePattern_tuple[0][3] = damagePattern_tuple[0][2] * damagePattern_tuple[0][1]
            # damagePattern_tuple[1]
            attr = "armor%sDamageResonance" % damagePattern_tuple[1][0].capitalize()
            damagePattern_tuple[1][1] = fit.ship.getModifiedItemAttr(attr)
            damagePattern_tuple[1][3] = damagePattern_tuple[1][2] * damagePattern_tuple[1][1]
            # damagePattern_tuple[2]
            attr = "armor%sDamageResonance" % damagePattern_tuple[2][0].capitalize()
            damagePattern_tuple[2][1] = fit.ship.getModifiedItemAttr(attr)
            damagePattern_tuple[2][3] = damagePattern_tuple[2][2] * damagePattern_tuple[2][1]
            # damagePattern_tuple[3]
            attr = "armor%sDamageResonance" % damagePattern_tuple[3][0].capitalize()
            damagePattern_tuple[3][1] = fit.ship.getModifiedItemAttr(attr)
            damagePattern_tuple[3][3] = damagePattern_tuple[3][2] * damagePattern_tuple[3][1]

            damagePattern_tuple = sorted(damagePattern_tuple, key=lambda damagePattern_tuple: damagePattern_tuple[3])

            logger.debug("damageType | resistAmount | damagePatternAmount |  modifiedDamageAmount | reactiveAmount")
            for damageType_tuple in damagePattern_tuple:
                logger.debug("%s | %f | %f | %f | %f", damageType_tuple[0], damageType_tuple[1], damageType_tuple[2],damageType_tuple[3],damageType_tuple[4])

            if damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount:
                # If damage pattern is even across the board, we "reset" back to default resists.
                logger.debug("Setting adaptivearmorhardener resists to uniform profile.")
                damagePattern_tuple[0][4]=.85
                damagePattern_tuple[1][4]=.85
                damagePattern_tuple[2][4]=.85
                damagePattern_tuple[3][4]=.85
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
                logger.debug("Setting adaptivearmorhardener resists to multiple damage profile.")
                if damagePattern_tuple[1][4] == 1 == damagePattern_tuple[0][4]:
                    logger.debug("We've run out of resists to steal. Breaking out of RAH cycle.")
                    break
                elif damagePattern_tuple[0][4] == 1:
                    countPasses = countPasses+1
                    # If our weakest resist is at 0, and we're still looping, bail out after we've tried this a few times.
                    # Most likely the RAH is cycling between two different profiles and is in an infinite loop.
                    if countPasses == 15:
                        logger.debug("Looped %f times. Most likely the RAH is cycling between two different profiles and is in an infinite loop. Breaking out of RAH cycle.", countPasses)
                        break
                    else:
                        pass

                if damagePattern_tuple[0][4] < .97:
                    # If there is more than 3% to steal, let's steal 3% and reduce the resit by that amount.
                    vampDmgOne = .03
                    damagePattern_tuple[0][4] = damagePattern_tuple[0][4] + .03
                else:
                    # If there is equal to or less than 3% left to steal, grab what we can and set the resist to 0%.
                    vampDmgOne = 1-damagePattern_tuple[0][4]
                    damagePattern_tuple[0][4] = 1

                if damagePattern_tuple[1][4] < .97:
                    # If there is more than 3% to steal, let's steal 3% and reduce the resit by that amount.
                    vampDmgTwo = .03
                    damagePattern_tuple[1][4] = damagePattern_tuple[1][4] + .03
                else:
                    # If there is equal to or less than 3% left to steal, grab what we can and set the resist to 0%.
                    vampDmgTwo = 1-damagePattern_tuple[1][4]
                    damagePattern_tuple[1][4] = 1

                #Add up the two amounts we stole, and divide it equally between the two
                vampDmgTotal = vampDmgOne + vampDmgTwo
                vampDmgTotal = vampDmgTotal / 2
                logger.debug("Vamped %f from %f and %f", vampDmgTotal*2, vampDmgOne, vampDmgTwo)

                damagePattern_tuple[2][4] = damagePattern_tuple[2][4] - vampDmgTotal
                damagePattern_tuple[3][4] = damagePattern_tuple[3][4] - vampDmgTotal



            logger.debug("Setting new resist profile.")
            for damagePatternType in damagePattern_tuple:
                attr = "armor%sDamageResonance" % damagePatternType[0].capitalize()
                module.forceItemAttr(attr, damagePatternType[4])
                fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup="preMul")
                #logger.debug("%s: %f", attr, damagePatternType[4])
