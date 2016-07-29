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
        logger.debug("Damage Pattern: %f\%f\%f\%f", damagePattern.emAmount, damagePattern.thermalAmount, damagePattern.kineticAmount, damagePattern.explosiveAmount)
        logger.debug("Original Armor Resists: %f\%f\%f\%f", fit.ship.getModifiedItemAttr('armorEmDamageResonance'), fit.ship.getModifiedItemAttr('armorThermalDamageResonance'), fit.ship.getModifiedItemAttr('armorKineticDamageResonance'), fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance'))

        # Populate a tuple with the damage profile modified by current armor resists.
        # We do _NOT_ account for the existing RAH adjustment, which it would in game. This means our values are slightly off,
        # but it's currently impossible to simulate in Pyfa.
        damagePattern_tuples  = [
            ('Em', damagePattern.emAmount*fit.ship.getModifiedItemAttr('armorEmDamageResonance')),
            ('Thermal', damagePattern.thermalAmount*fit.ship.getModifiedItemAttr('armorThermalDamageResonance')),
            ('Kinetic', damagePattern.kineticAmount*fit.ship.getModifiedItemAttr('armorKineticDamageResonance')),
            ('Explosive', damagePattern.explosiveAmount*fit.ship.getModifiedItemAttr('armorExplosiveDamageResonance')),
        ]

        logger.debug("Damage Adjusted for Armor Resists: %f\%f\%f\%f", damagePattern_tuples[0][1], damagePattern_tuples[1][1], damagePattern_tuples[2][1], damagePattern_tuples[3][1])

        # Sort the tuple to drop the highest damage value to the bottom
        sortedDamagePattern_tuples = sorted(damagePattern_tuples, key=lambda damagePattern: damagePattern[1])

        if damagePattern.emAmount == damagePattern.thermalAmount == damagePattern.kineticAmount == damagePattern.explosiveAmount:
            # If damage pattern is even across the board, we "reset" back to default resists.
            logger.debug("Setting adaptivearmorhardener resists to uniform profile.")
            adjustedDamagePattern_tuples = [
                (sortedDamagePattern_tuples[0][0], .85),
                (sortedDamagePattern_tuples[1][0], .85),
                (sortedDamagePattern_tuples[2][0], .85),
                (sortedDamagePattern_tuples[3][0], .85),
            ]
        else:
            if sortedDamagePattern_tuples[2][1] == 0:
                # Per CCP Larrikin: when RAH takes single damage type, that damage type goes to 60% resists.
                logger.debug("Setting adaptivearmorhardener resists to single damage profile.")
                adjustedDamagePattern_tuples = [
                    (sortedDamagePattern_tuples[0][0], 1),
                    (sortedDamagePattern_tuples[1][0], 1),
                    (sortedDamagePattern_tuples[2][0], 1),
                    (sortedDamagePattern_tuples[3][0], .40),
                ]
            else:
                # Per CCP Larrikin: when RAH takes mixed damage, the two highest damage values will get 30% resists and two lowest get 0% resists.
                logger.debug("Setting adaptivearmorhardener resists to mixed damage profile.")
                adjustedDamagePattern_tuples = [
                    (sortedDamagePattern_tuples[0][0], 1),
                    (sortedDamagePattern_tuples[1][0], 1),
                    (sortedDamagePattern_tuples[2][0], .70),
                    (sortedDamagePattern_tuples[3][0], .70),
                ]

        logger.debug("Setting new resist profile.")
        for damagePatternType in adjustedDamagePattern_tuples:
            attr = "armor%sDamageResonance" % damagePatternType[0].capitalize()
            module.forceItemAttr(attr, damagePatternType[1])
            fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr), stackingPenalties=True, penaltyGroup="preMul")
            logger.debug("%s: %f", attr, damagePatternType[1])

