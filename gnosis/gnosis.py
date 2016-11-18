"""
Integrates Gnosis into Pyfa
"""

from EVE_Gnosis.formulas.formulas import Formulas
from EVE_Gnosis.simulations.capacitor import Capacitor


class GnosisFormulas:
    def __init__(self):
        pass

    @staticmethod
    def get_peak_regen(capacity, recharge_rate):
        return_matrix = Formulas.capacitor_shield_regen_matrix(capacity, recharge_rate)
        high_water_delta = high_water = 0
        for item in return_matrix:
            if high_water_delta < item['DeltaAmount']:
                high_water_delta = item['DeltaAmount']
                high_water = item

        if high_water:
            return high_water
        else:
            return False


class GnosisSimulation:
    def __init__(self):
        pass

    @staticmethod
    def capacitor_simulation(fit, projected_items, capacity, recharge_rate):
        module_list = []
        for module in fit.modules:
            if module.getModifiedItemAttr("capacitorNeed") and getattr(module, 'state', None) > 0:
                capacitor_need = module.getModifiedItemAttr(
                    "capacitorNeed") * -1  # Turn drains into negative and boosts to positive
                duration_one = module.getModifiedItemAttr("duration")
                duration_two = module.getModifiedItemAttr("speed")
                duration = max(duration_one, duration_two, 0)
                charges = getattr(module, 'numCharges', None)
                reload_time_one = module.getModifiedItemAttr("reloadTime")
                reload_time_two = getattr(module, 'reloadTime', None)
                reactivation_delay = module.getModifiedItemAttr("moduleReactivationDelay")

                reload_time = max(reload_time_one, reload_time_two, 0)

                if not reload_time:
                    reload_time = False

                if not charges:
                    charges = False

                if not reactivation_delay:
                    reactivation_delay = False

                if reload_time and reactivation_delay:
                    reload_time = max(reload_time, reactivation_delay)
                    reactivation_delay = False

                if capacitor_need and duration:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                            'ReactivationDelay': reactivation_delay,
                        }
                    )

        for item in projected_items:
            projected_src, duration, capacitor_need, charges = item

            # Turn drains into negative and boosts to positive
            if not capacitor_need:
                amount_one = projected_src.getModifiedItemAttr("fighterAbilityEnergyNeutralizerAmount")
                amount_two = projected_src.getModifiedItemAttr("energyNeutralizerAmount")
                amount_three = projected_src.getModifiedItemAttr("powerTransferAmount")
                capacitor_need = max(amount_one, amount_two, amount_three, 0) * -1
            else:
                capacitor_need *= -1

            if capacitor_need and getattr(projected_src, 'state', 1) == 1:
                if not duration:
                    duration_one = projected_src.getModifiedItemAttr("duration")
                    duration_two = projected_src.getModifiedItemAttr("speed")
                    duration = max(duration_one, duration_two, 0)

                if not charges:
                    charges = getattr(projected_src, 'numCharges', None)

                reload_time_one = projected_src.getModifiedItemAttr("reloadTime")
                reload_time_two = getattr(projected_src, 'reloadTime', None)
                reactivation_delay = projected_src.getModifiedItemAttr("moduleReactivationDelay")

                reload_time = max(reload_time_one, reload_time_two, 0)

                if not reload_time:
                    reload_time = False

                if not charges:
                    charges = False

                if not reactivation_delay:
                    reactivation_delay = False

                if reload_time and reactivation_delay:
                    reload_time = max(reload_time, reactivation_delay)
                    reactivation_delay = False

                if capacitor_need and duration:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                            'ReactivationDelay': reactivation_delay,
                        }
                    )

        return_matrix = Capacitor.capacitor_time_simulator(module_list, capacity, recharge_rate)

        return {'ModuleDict': module_list, 'Matrix': return_matrix}
