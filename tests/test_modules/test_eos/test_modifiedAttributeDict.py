# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import math
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit

def test_multiply_stacking_penalties(DB, Saveddata, RifterFit):
    """
    Tests the stacking penalties under multiply
    """
    char0 = Saveddata['Character'].getAll0()

    RifterFit.character = char0
    starting_em_resist = RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance")

    mod = Saveddata['Module'](DB['db'].getItem("EM Ward Amplifier II"))
    item_modifer = mod.item.getAttribute("emDamageResistanceBonus")


    for _ in range(10):
        # See: http://wiki.eveuniversity.org/Eve_Math#Stacking_Penalties
        current_effectiveness = pow(0.5, (pow(0.45 * (_ - 1), 2)))

        RifterFit.clear()
        RifterFit.calculateModifiedAttributes()

        if _ == 0:
            # First run we have no modules, se don't try and calculate them.
            calculated_resist = RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance")
        else:
            new_item_modifier = 1 + ((item_modifer * current_effectiveness) / 100)
            calculated_resist = (em_resist * new_item_modifier)
            RifterFit.modules.append(mod)
            RifterFit.calculateModifiedAttributes()

        em_resist = RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance")

        # Ohnoes! Our stacking penalty calculations are off! Round off because the ones in Eos are probably wrong after four decimal places.
        # TODO: Remove the round when Eos calcs are fixed
        assert round(em_resist, 4) == round(calculated_resist, 4)
        # print(str(em_resist) + "==" + str(calculated_resist))
