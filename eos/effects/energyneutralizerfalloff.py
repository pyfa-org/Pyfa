# energyNeutralizerFalloff
#
# Used by:
# Modules from group: Energy Neutralizer (51 of 51)
from eos.types import State
type = "active", "projected"
def handler(fit, module, context):
    if "projected" in context and ((hasattr(module, "state") \
    and module.state >= State.ACTIVE) or hasattr(container, "amountActive")):
        amount = module.getModifiedItemAttr("energyNeutralizerAmount")
        time = module.getModifiedItemAttr("duration")
        rigSize = fit.ship.getModifiedItemAttr("rigSize")
        modifierLarge = module.getModifiedItemAttr("entityCapacitorLevelModifierLarge")
        modifierMedium = module.getModifiedItemAttr("entityCapacitorLevelModifierMedium")
        modifierSmall = module.getModifiedItemAttr("entityCapacitorLevelModifierSmall")
        energyNeutralizerSignatureResolution = module.getModifiedItemAttr("energyNeutralizerSignatureResolution")
        signatureRadius = fit.ship.getModifiedItemAttr("signatureRadius")

        #Signature reduction, uses the bomb formula as per CCP Larrikin
        if energyNeutralizerSignatureResolution:
            sigRatio = signatureRadius/energyNeutralizerSignatureResolution

            sigReductionList = [1, sigRatio]
            amount = amount*min(sigReductionList)

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

