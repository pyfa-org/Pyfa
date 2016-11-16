"""
Integrates Gnosis into Pyfa
"""

from EVE_Gnosis.formulas.formulas import Formulas
from EVE_Gnosis.simulations.capacitor import Capacitor


class GnosisFormulas():

    @staticmethod
    def get_peak_regen(capacity, recharge_rate):
        return_matrix = Formulas.capacitor_shield_regen_matrix(capacity,recharge_rate)
        high_water_percent = 0
        high_water_delta = 0
        for item in return_matrix:
            if high_water_delta < item['DeltaAmount']:
                high_water = item

        if high_water:
            return high_water
        else:
            return False

class GnosisSimulation():
    @staticmethod
    def capacitor_simulation(fit, capacity, recharge_rate):
        module_list = []

        for module in fit.modules:
            if module.getModifiedItemAttr("capacitorNeed") and getattr(module, 'state', None) == 1:
                capacitor_need = module.getModifiedItemAttr("capacitorNeed") * -1  # Turn drains into negative and boosts to positive
                duration = module.getModifiedItemAttr("duration")
                charges = getattr(module, 'numCharges', None)
                reload_time_one = module.getModifiedItemAttr("reloadTime")
                reload_time_two = getattr(module, 'reloadTime', None)
                reactivation_delay = module.getModifiedItemAttr("moduleReactivationDelay")

                reload_time = max(reload_time_one, reload_time_two, reactivation_delay, 0)

                if not reload_time:
                    reload_time = False

                if not charges:
                        charges = False

                peak_regen = GnosisFormulas.get_peak_regen(capacity, recharge_rate)



                if capacitor_need:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                        }
                    )

        test = fit.projectedModules
        '''
        for projected_ship in fit.victimOf:
            for projected_ship.source_fit.
            fit
        '''

        return_matrix = Capacitor.capacitor_time_simulator(module_list, capacity, recharge_rate)

        return return_matrix