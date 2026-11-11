from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from eos import effects


@pytest.mark.parametrize(('effect', 'marker', 'bonus', 'increment'), [
    pytest.param(effects.Effect12969, 'rigSetGallenteNavyModule', 'repairBonus', 1, id='federation-navy'),
    pytest.param(effects.Effect12982, 'rigSetAmarrNavyModule', 'capNeedBonus', -1, id='imperial-navy'),
    pytest.param(effects.Effect12984, 'rigSetMinmatarFleetModule', 'durationSkillBonus', -1, id='republic-fleet'),
    pytest.param(effects.Effect12985, 'rigSetCaldariNavyModule', 'shieldCapacityBonus', 1, id='caldari-navy'),
    pytest.param(effects.Effect13000, 'rigSetDarkBloodModule', 'rigEnergyTurretDamageBonus', 1, id='dark-blood'),
    pytest.param(effects.Effect13006, 'rigSetTrueSanshaModule', 'trackingSpeedBonus', 1, id='true-sansha'),
    pytest.param(
        effects.Effect13008, 'rigSetShadowSerpentisModule', 'rigStasisWebResistance', -1, id='shadow-serpentis'),
    pytest.param(effects.Effect13012, 'rigSetDreadGuristasModule', 'emDamageResistanceBonus', -1, id='dread-guristas'),
    pytest.param(effects.Effect13016, 'rigSetDominationAngelModule', 'rigSignatureRadiusBonus', -1, id='domination'),
])
def test_synchronizer_does_not_count_mutated_modules(effect, marker, bonus, increment):
    # Both modules retain the faction marker, but only the ordinary module counts.
    modules = [SimpleNamespace(
        isEmpty=False,
        isMutated=mutated,
        getModifiedItemAttr=lambda key, default=0: 1 if key == marker else default,
    ) for mutated in (False, True)]
    fit = SimpleNamespace(modules=modules)
    synchronizer = Mock()

    effect.handler(fit, synchronizer, ('module',), None)

    synchronizer.increaseItemAttr.assert_any_call(bonus, increment)
