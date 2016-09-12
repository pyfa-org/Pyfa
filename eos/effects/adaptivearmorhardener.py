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
        while runLoop == 1:
            damagePattern_tuple = sorted(damagePattern_tuple, key=lambda damagePattern_tuple: damagePattern_tuple[3])

            logger.debug("damageType | resistAmount | damagePatternAmount |  modifiedDamageAmount | reactiveAmount")
            for damageType_tuple in damagePattern_tuple:
                logger.debug("%s | %f | %f | %f | %f", damageType_tuple[0], damageType_tuple[1], damageType_tuple[2],damageType_tuple[3],damageType_tuple[4])

            if damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount:
                # If damage pattern is even across the board, we "reset" back to default resists.
                logger.debug("Setting adaptivearmorhardener resists to uniform profile.")
                adjustedDamagePattern_tuples = [
                    (damagePattern_tuple[0][4], .85),
                    (damagePattern_tuple[1][4], .85),
                    (damagePattern_tuple[2][4], .85),
                    (damagePattern_tuple[3][4], .85),
                ]
                runLoop = 0
            else:
                if damagePattern_tuple[1][4] == 1 == damagePattern_tuple[0][4]:
                    # We've run out of resists to steal.
                    break
                elif damagePattern_tuple[0][4] == 1:
                    # Need to figure out something clever here to prevent infinite loops
                    pass

                if damagePattern_tuple[0][4] < .97:
                    vampDmgOne = .03
                    damagePattern_tuple[0][4] = damagePattern_tuple[0][4] + .03
                else:
                    vampDmgOne = 1-damagePattern_tuple[0][4]
                    damagePattern_tuple[0][4] = 1

                if damagePattern_tuple[1][4] < .97:
                    vampDmgTwo = .03
                    damagePattern_tuple[1][4] = damagePattern_tuple[1][4] + .03
                else:
                    vampDmgTwo = 1-damagePattern_tuple[1][4]
                    damagePattern_tuple[1][4] = 1

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
