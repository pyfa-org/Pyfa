import heapq
import time
from math import sqrt, exp
from collections import Counter

DAY = 24 * 60 * 60 * 1000


def lcm(a, b):
    n = a * b
    while b:
        a, b = b, a % b
    return n / a


class CapSimulator:
    """Entity's EVE Capacitor Simulator"""

    def __init__(self):
        # simulator defaults (change in instance, not here)

        self.capacitorCapacity = 100
        self.capacitorRecharge = 1000
        self.startingCapacity = 1000

        # max simulated time.
        self.t_max = DAY

        # take reloads into account?
        self.reload = False

        # stagger activations of identical modules?
        self.stagger = False

        # scale activation duration and capNeed to values that ease the
        # calculation at the cost of accuracy?
        self.scale = False

        # millisecond resolutions for scaling
        self.scale_resolutions = (100, 50, 25, 10)

        # relevant decimal digits of capacitor for LCM period optimization
        self.stability_precision = 1

        # Stores how cap sim changed cap values outside of cap regen time
        self.saved_changes = ()
        self.saved_changes_internal = None

        # Reports if sim was stopped due to detecting stability early
        self.optimize_repeats = True
        self.result_optimized_repeats = None

    def scale_activation(self, duration, capNeed):
        for res in self.scale_resolutions:
            mod = duration % res
            if mod:
                if mod > res / 2.0:
                    mod = res - mod
                else:
                    mod = -mod

                if abs(mod) <= duration / 100.0:
                    # only adjust if the adjustment is less than 1%
                    duration += mod
                    capNeed += float(mod) / duration * capNeed
                    break

        return duration, capNeed

    def init(self, modules):
        """prepare modules. a list of (duration, capNeed, clipSize, disableStagger, reloadTime, isInjector) tuples is
         expected, with clipSize 0 if the module has infinite ammo.
            """
        self.modules = modules

    def reset(self):
        """Reset the simulator state"""
        self.state = []
        self.saved_changes_internal = {}
        self.result_optimized_repeats = False
        mods = {}
        period = 1
        disable_period = False

        # Loop over modules, clearing clipSize if applicable, and group modules based on attributes
        for (duration, capNeed, clipSize, disableStagger, reloadTime, isInjector) in self.modules:
            if self.scale:
                duration, capNeed = self.scale_activation(duration, capNeed)

            # set clipSize to infinite if reloads are disabled unless it's
            # a cap booster module
            if not self.reload and not isInjector:
                clipSize = 0
                reloadTime = 0

            # Group modules based on their properties
            key = (duration, capNeed, clipSize, disableStagger, reloadTime, isInjector)
            if key in mods:
                mods[key] += 1
            else:
                mods[key] = 1

        # Loop over grouped modules, configure staggering and push to the simulation state
        for (duration, capNeed, clipSize, disableStagger, reloadTime, isInjector), amount in mods.items():
            # period optimization doesn't work when reloads are active.
            if clipSize:
                disable_period = True
            # Just push multiple instances if item is injector. We do not want to stagger them as we will
            # use them as needed and want them to be available right away
            if isInjector:
                for i in range(amount):
                    heapq.heappush(self.state, [0, duration, capNeed, 0, clipSize, reloadTime, isInjector])
                continue
            if self.stagger and not disableStagger:
                # Stagger all mods if they do not need to be reloaded
                if clipSize == 0:
                    duration = int(duration / amount)
                # Stagger mods after first
                else:
                    stagger_amount = (duration * clipSize + reloadTime) / (amount * clipSize)
                    for i in range(1, amount):
                        heapq.heappush(self.state, [i * stagger_amount, duration, capNeed, 0, clipSize, reloadTime, isInjector])
            # If mods are not staggered - just multiply cap use
            else:
                capNeed *= amount

            period = lcm(period, duration)

            heapq.heappush(self.state, [0, duration, capNeed, 0, clipSize, reloadTime, isInjector])

        if disable_period:
            self.period = self.t_max
        else:
            self.period = period

    def run(self):
        """Run the simulation"""

        start = time.time()
        awaitingInjectors = []
        awaitingInjectorsCounterWrap = Counter()
        self.reset()

        push = heapq.heappush
        pop = heapq.heappop

        state = self.state
        stability_precision = self.stability_precision
        period = self.period

        activation = None
        iterations = 0

        capCapacity = self.capacitorCapacity
        tau = self.capacitorRecharge / 5.0

        cap_wrap = self.startingCapacity  # cap value at last period
        cap_lowest = self.startingCapacity  # lowest cap value encountered
        cap_lowest_pre = self.startingCapacity  # lowest cap value before activations
        cap = self.startingCapacity  # current cap value
        t_wrap = self.period  # point in time of next period
        t_last = 0
        t_max = self.t_max

        while 1:
            # Nothing to pop - might happen when no mods are activated, or when
            # only cap injectors are active (and are postponed by code below)
            try:
                activation = pop(state)
            except IndexError:
                break
            t_now, duration, capNeed, shot, clipSize, reloadTime, isInjector = activation

            # Max time reached, stop simulation - we're stable
            if t_now >= t_max:
                break

            # Regenerate cap from last time point
            if t_now > t_last:
                cap = ((1.0 + (sqrt(cap / capCapacity) - 1.0) * exp((t_last - t_now) / tau)) ** 2) * capCapacity

            if t_now != t_last:
                if cap < cap_lowest_pre:
                    cap_lowest_pre = cap
                if t_now == t_wrap:
                    # history is repeating itself, so if we have more cap now than last
                    # time this happened, it is a stable setup.
                    awaitingInjectorsCounterNow = Counter(awaitingInjectors)
                    if self.optimize_repeats and cap >= cap_wrap and awaitingInjectorsCounterNow == awaitingInjectorsCounterWrap:
                        self.result_optimized_repeats = True
                        break
                    cap_wrap = round(cap, stability_precision)
                    awaitingInjectorsCounterWrap = awaitingInjectorsCounterNow
                    t_wrap += period

            t_last = t_now
            iterations += 1

            # If injecting cap will "overshoot" max cap, postpone it
            if isInjector and cap - capNeed > capCapacity:
                awaitingInjectors.append((duration, capNeed, shot, clipSize, reloadTime, isInjector))

            else:
                # If we will need more cap than we have, but we are not at 100% -
                # use awaiting cap injectors to top us up until we have enough or
                # until we're full
                if capNeed > cap and cap < capCapacity:
                    while awaitingInjectors and capNeed > cap and capCapacity > cap:
                        neededInjection = min(capNeed - cap, capCapacity - cap)
                        # Find injectors which have just enough cap or more
                        goodInjectors = [i for i in awaitingInjectors if -i[1] >= neededInjection]
                        if goodInjectors:
                            # Pick injector which overshoots the least
                            bestInjector = min(goodInjectors, key=lambda i: -i[1])
                        else:
                            # Take the one which provides the most cap
                            bestInjector = max(goodInjectors, key=lambda i: -i[1])
                        # Use injector
                        awaitingInjectors.remove(bestInjector)
                        inj_duration, inj_capNeed, inj_shot, inj_clipSize, inj_reloadTime, inj_isInjector = bestInjector
                        cap -= inj_capNeed
                        if cap > capCapacity:
                            cap = capCapacity
                        self.saved_changes_internal[t_now] = cap
                        # Add injector to regular state tracker
                        inj_t_now = t_now
                        inj_t_now += inj_duration
                        inj_shot += 1
                        if inj_clipSize:
                            if inj_shot % inj_clipSize == 0:
                                inj_shot = 0
                                inj_t_now += inj_reloadTime
                        push(state, [inj_t_now, inj_duration, inj_capNeed, inj_shot, inj_clipSize, inj_reloadTime, inj_isInjector])

                # Apply cap modification
                cap -= capNeed
                if cap > capCapacity:
                    cap = capCapacity
                self.saved_changes_internal[t_now] = cap

                if cap < cap_lowest:
                    # Negative cap - we're unstable, simulation is over
                    if cap < 0.0:
                        break
                    cap_lowest = cap

                # Try using awaiting injectors to top up the cap after spending some
                while awaitingInjectors and cap < capCapacity:
                    neededInjection = capCapacity - cap
                    # Find injectors which do not overshoot max cap
                    goodInjectors = [i for i in awaitingInjectors if -i[1] <= neededInjection]
                    if not goodInjectors:
                        break
                    # Take the one which provides the most cap
                    bestInjector = max(goodInjectors, key=lambda i: -i[1])
                    # Use injector
                    awaitingInjectors.remove(bestInjector)
                    inj_duration, inj_capNeed, inj_shot, inj_clipSize, inj_reloadTime, inj_isInjector = bestInjector
                    cap -= inj_capNeed
                    if cap > capCapacity:
                        cap = capCapacity
                    self.saved_changes_internal[t_now] = cap
                    # Add injector to regular state tracker
                    inj_t_now = t_now
                    inj_t_now += inj_duration
                    inj_shot += 1
                    if inj_clipSize:
                        if inj_shot % inj_clipSize == 0:
                            inj_shot = 0
                            inj_t_now += inj_reloadTime
                    push(state, [inj_t_now, inj_duration, inj_capNeed, inj_shot, inj_clipSize, inj_reloadTime, inj_isInjector])

                # queue the next activation of this module
                t_now += duration
                shot += 1
                if clipSize:
                    if shot % clipSize == 0:
                        shot = 0
                        t_now += reloadTime  # include reload time
                activation[0] = t_now
                activation[3] = shot

                push(state, activation)
        if activation is not None:
            push(state, activation)

        # update instance with relevant results.
        self.t = t_last
        self.iterations = iterations

        # calculate EVE's stability value
        try:
            avgDrain = sum(x[2] / x[1] for x in self.state)
            self.cap_stable_eve = 0.25 * (1.0 + sqrt(-(2.0 * avgDrain * tau - capCapacity) / capCapacity)) ** 2
        except ValueError:
            self.cap_stable_eve = 0.0

        if cap > 0.0:
            # capacitor low/high water marks
            self.cap_stable_low = cap_lowest
            self.cap_stable_high = cap_lowest_pre
        else:
            self.cap_stable_low = self.cap_stable_high = 0.0

        self.saved_changes = tuple((k / 1000, max(0, self.saved_changes_internal[k])) for k in sorted(self.saved_changes_internal))
        self.saved_changes_internal = None

        self.runtime = time.time() - start
