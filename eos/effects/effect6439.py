# fighterAbilityEvasiveManeuvers
#
# Used by:
# Fighters from group: Light Fighter (16 of 32)
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
displayName = "Evasive Maneuvers"

prefix = "fighterAbilityEvasiveManeuvers"

# Is ability applied to the fighter squad as a whole, or per fighter?
grouped = True

type = "active"
runTime = "late"


def handler(fit, container, context):
    container.boostItemAttr("maxVelocity",
                            container.getModifiedItemAttr("fighterAbilityEvasiveManeuversSpeedBonus"))
    container.boostItemAttr("signatureRadius",
                            container.getModifiedItemAttr("fighterAbilityEvasiveManeuversSignatureRadiusBonus"),
                            stackingPenalties=True)

    # These may not have stacking penalties, but there's nothing else that affects the attributes yet to check.
    container.multiplyItemAttr("shieldEmDamageResonance",
                               container.getModifiedItemAttr("fighterAbilityEvasiveManeuversEmResonance"),
                               stackingPenalties=True)
    container.multiplyItemAttr("shieldThermalDamageResonance",
                               container.getModifiedItemAttr("fighterAbilityEvasiveManeuversThermResonance"),
                               stackingPenalties=True)
    container.multiplyItemAttr("shieldKineticDamageResonance",
                               container.getModifiedItemAttr("fighterAbilityEvasiveManeuversKinResonance"),
                               stackingPenalties=True)
    container.multiplyItemAttr("shieldExplosiveDamageResonance",
                               container.getModifiedItemAttr("fighterAbilityEvasiveManeuversExpResonance"),
                               stackingPenalties=True)
