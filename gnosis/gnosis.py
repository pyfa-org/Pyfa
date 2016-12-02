"""
Integrates Gnosis into Pyfa
"""

from EVE_Gnosis.formulas.formulas import Formulas
from EVE_Gnosis.simulations.capacitor import Capacitor

import sys
test = True
#import service
#try:
#    import service
#except ImportError:
#    import sys
#    Service = sys.modules['service']

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
    def capacitor_simulation(fit, projected_capacitor, capacity, recharge_rate, add_reactivation_delay=None):

        sFit = service.Fit.getInstance()

        # Get user preferences for running the Gnosis engine
        setting_factor_reload_time = sFit.serviceFittingOptions["useGlobalForceReload"]

        module_list = []
        for module in fit.modules:

            if getattr(module, 'state', 0) > 0:

                # Get capacitor usage
                capacitor_need = module.getModifiedItemAttr("capacitorNeed")
                if capacitor_need:
                    # Turn drains into negative and boosts to positive
                    capacitor_need *= -1
                else:
                    capacitor_need = 0

                # Get how long the module takes to cycle
                duration_one = module.getModifiedItemAttr("duration")
                duration_two = module.getModifiedItemAttr("speed")
                duration = max(duration_one, duration_two, 0)

                if setting_factor_reload_time:
                    # Get number of charges/reloads
                    charges = getattr(module, 'numCharges', None)
                    if not charges:
                        charges = False

                    # Get reload time
                    reload_time_one = module.getModifiedItemAttr("reloadTime")
                    reload_time_two = getattr(module, 'reloadTime', None)
                    reload_time = max(reload_time_one, reload_time_two, 0)
                    if not reload_time:
                        reload_time = False
                else:
                    charges = False
                    reload_time = False

                # Get reactivation delay
                reactivation_delay = module.getModifiedItemAttr("moduleReactivationDelay")
                if not reactivation_delay:
                    reactivation_delay = False

                # Get rep amounts
                shield_reps = module.getModifiedItemAttr("shieldBonus")
                if not shield_reps:
                    shield_reps = False

                armor_reps = module.getModifiedItemAttr("armorDamageAmount")
                if not armor_reps:
                    armor_reps = False

                hull_reps = module.getModifiedItemAttr("structureDamageAmount")
                if not hull_reps:
                    hull_reps = False

                # Catch modules with no charges but a reload time
                # Mostly will be empty Anciliary repairers
                if not charges and reload_time:
                    reload_time = False

                # Add in the passed in additional reactivation delay
                # This is used for calculating cap stability with modules running
                # We only want to target local modules that use cap and do not have
                # a reactivation delay
                if capacitor_need < 0 and not reactivation_delay and add_reactivation_delay:
                    reactivation_delay = add_reactivation_delay

                if (capacitor_need and duration) is not None:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                            'ReactivationDelay': reactivation_delay,
                            'ShieldRepair': shield_reps,
                            'ArmorRepair': armor_reps,
                            'HullRepair': hull_reps,
                        }
                    )

        # Projected neuts, nos, and cap transfers
        for item in projected_capacitor:
            projected_src, duration, capacitor_need, charges = item

            # Turn drains into negative and boosts to positive
            if not capacitor_need:
                amount_one = projected_src.getModifiedItemAttr("fighterAbilityEnergyNeutralizerAmount")
                amount_two = projected_src.getModifiedItemAttr("energyNeutralizerAmount")
                amount_three = projected_src.getModifiedItemAttr("powerTransferAmount")
                capacitor_need = max(amount_one, amount_two, amount_three, 0) * -1
            else:
                capacitor_need *= -1

            if getattr(projected_src, 'state', 0) > 0:
                if not duration:
                    duration_one = projected_src.getModifiedItemAttr("duration")
                    duration_two = projected_src.getModifiedItemAttr("speed")
                    duration = max(duration_one, duration_two, 0)

                if setting_factor_reload_time:
                    if not charges:
                        # Get number of charges/reloads
                        charges = getattr(projected_src, 'numCharges', None)
                    if not charges:
                        charges = False

                    reload_time_one = projected_src.getModifiedItemAttr("reloadTime")
                    reload_time_two = getattr(projected_src, 'reloadTime', None)
                    reload_time = max(reload_time_one, reload_time_two, 0)
                    if not reload_time:
                        reload_time = False
                else:
                    charges = False
                    reload_time = False

                reactivation_delay = projected_src.getModifiedItemAttr("moduleReactivationDelay")
                if not reactivation_delay:
                    reactivation_delay = False

                if capacitor_need and duration:
                    module_list.append(
                        {
                            'Amount': capacitor_need,
                            'CycleTime': duration,
                            'Charges': charges,
                            'ReloadTime': reload_time,
                            'ReactivationDelay': reactivation_delay,
                            'Projected': True,
                        }
                    )

        for projection_extraAttributes_type in (
                'shieldRepair',
                'armorRepair',
                'hullRepair',
        ):
            for projecting_fit, afflictors in fit.extraAttributes.getAfflictions(
                    projection_extraAttributes_type).iteritems():
                if projecting_fit == fit:
                    # We can see local modules projected back on the fit. This is bad. Don't do this.
                    pass
                else:
                    for afflictor, modifier, amount, used in afflictors:
                        # Get capacitor usage
                        # Projected modules never use cap, as cap trans is handed under __drains
                        capacitor_need = 0

                        # Get how long the module takes to cycle
                        duration_one = afflictor.getModifiedItemAttr("duration")
                        duration_two = afflictor.getModifiedItemAttr("speed")
                        duration = max(duration_one, duration_two, 0)

                        if setting_factor_reload_time:
                            # Get number of charges/reloads
                            charges = getattr(afflictor, 'numCharges', None)
                            if not charges:
                                charges = False

                            # Get reload time
                            reload_time_one = afflictor.getModifiedItemAttr("reloadTime")
                            reload_time_two = getattr(afflictor, 'reloadTime', None)
                            reload_time = max(reload_time_one, reload_time_two, 0)
                            if not reload_time:
                                reload_time = False
                        else:
                            charges = False
                            reload_time = False

                        # Get reactivation delay
                        reactivation_delay = afflictor.getModifiedItemAttr("moduleReactivationDelay")
                        if not reactivation_delay:
                            reactivation_delay = False

                        # Get rep amounts
                        shield_reps = afflictor.getModifiedItemAttr("shieldBonus")
                        if not shield_reps:
                            shield_reps = False

                        armor_reps = afflictor.getModifiedItemAttr("armorDamageAmount")
                        if not armor_reps:
                            armor_reps = False

                        hull_reps = afflictor.getModifiedItemAttr("structureDamageAmount")
                        if not hull_reps:
                            hull_reps = False

                        # Catch modules with no charges but a reload time
                        # Mostly will be empty Anciliary repairers
                        if not charges and reload_time:
                            reload_time = False

                        # Add in the passed in additional reactivation delay
                        # This is used for calculating cap stability with modules running
                        # We only want to target local modules that use cap and do not have
                        # a reactivation delay
                        if capacitor_need < 0 and not reactivation_delay and add_reactivation_delay:
                            reactivation_delay = add_reactivation_delay

                        if (capacitor_need and duration) is not None:
                            module_list.append(
                                {
                                    'Amount': capacitor_need,
                                    'CycleTime': duration,
                                    'Charges': charges,
                                    'ReloadTime': reload_time,
                                    'ReactivationDelay': reactivation_delay,
                                    'ShieldRepair': shield_reps,
                                    'ArmorRepair': armor_reps,
                                    'HullRepair': hull_reps,
                                    'Projected': True,
                                }
                            )

        return_matrix = Capacitor.capacitor_time_simulator(module_list, capacity, recharge_rate)

        return {'ModuleDict': module_list, 'Matrix': return_matrix}
