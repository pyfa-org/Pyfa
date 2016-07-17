# entityEnergyNeutralizerFalloff
#
# Used by:
# Drones from group: Energy Neutralizer Drone (3 of 3)
from eos.types import State
type = "active", "projected"
def handler(fit, module, context):
    if "projected" in context and ((hasattr(module, "state") \
    and module.state >= State.ACTIVE) or hasattr(module, "amountActive")):
        amount = module.getModifiedItemAttr("energyNeutralizerAmount")
        time = module.getModifiedItemAttr("energyNeutralizerDuration")
        rigSize = fit.ship.getModifiedItemAttr("rigSize")
        modifierLarge = module.getModifiedItemAttr("entityCapacitorLevelModifierLarge")
        modifierMedium = module.getModifiedItemAttr("entityCapacitorLevelModifierMedium")
        modifierSmall = module.getModifiedItemAttr("entityCapacitorLevelModifierSmall")

        #Small rigged ships
        if (rigSize == 1) and modifierSmall:
            amount = amount*modifierSmall

        #Medium rigged ships
        if (rigSize == 2) and modifierMedium:
            amount = amount*modifierMedium

        #Large rigged ships
        if (rigSize == 3) and modifierLarge:
            amount = amount*modifierLarge

        fit.addDrain(time, amount, 0)
