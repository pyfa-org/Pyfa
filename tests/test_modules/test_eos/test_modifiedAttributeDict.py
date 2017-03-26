# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import math
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.realpath(os.path.join(script_dir, '..', '..', '..'))
print script_dir
sys.path.append(script_dir)

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

    RifterFit.calculateModifiedAttributes()

    for _ in range(10):
        if _ == 0:
            # First run we have no modules, se don't try and calculate them.
            calculated_resist = RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance")
        else:
            # Calculate what our next resist should be
            # Denominator: [math.exp((i / 2.67) ** 2.0) for i in xrange(8)]
            current_effectiveness = 1 / math.exp(((_ - 1) / 2.67) ** 2.0)
            new_item_modifier = 1 + ((item_modifer * current_effectiveness) / 100)
            calculated_resist = (em_resist * new_item_modifier)

            # Add another resist module to our fit.
            RifterFit.modules.append(mod)

        # Modify our fit so that Eos generates new numbers for us.
        RifterFit.clear()
        RifterFit.calculateModifiedAttributes()

        em_resist = RifterFit.ship.getModifiedItemAttr("shieldEmDamageResonance")

        assert em_resist == calculated_resist
        # print(str(em_resist) + "==" + str(calculated_resist))
