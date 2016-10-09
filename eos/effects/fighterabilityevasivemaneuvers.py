# Not used by any item
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
def handler(fit, module, context):
    module.boostItemAttr("maxVelocity", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversSpeedBonus"))
    module.boostItemAttr("signatureRadius", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversSignatureRadiusBonus"), stackingPenalties = True)
    
	# These may not have stacking penalties, but there's nothing else that affects the attributes yet to check.
    module.multiplyItemAttr("shieldEmDamageResonance", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversEmResonance"), stackingPenalties = True)
    module.multiplyItemAttr("shieldThermalDamageResonance", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversThermResonance"), stackingPenalties = True)
    module.multiplyItemAttr("shieldKineticDamageResonance", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversKinResonance"), stackingPenalties = True)
    module.multiplyItemAttr("shieldExplosiveDamageResonance", module.getModifiedItemAttr("fighterAbilityEvasiveManeuversExpResonance"), stackingPenalties = True)