import heapq
import time
from math import sqrt, exp

DAY = 24 * 60 * 60 * 1000


def lcm(a, b):
    n = a * b
    while b:
        a, b = b, a % b
    return n / a


class CapSimulator(object):
    """Entity's EVE Capacitor Simulator"""

    def __init__(self):
        # simulator defaults (change in instance, not here)

        self.capacitorCapacity = 100
        self.capacitorRecharge = 1000

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
        """prepare modules. a list of (duration, capNeed, clipSize, disableStagger) tuples is
         expected, with clipSize 0 if the module has infinite ammo.
            """
        self.modules = modules

    def reset(self):
        """Reset the simulator state"""
        self.state = []
        mods = {}
        period = 1
        disable_period = False

        # Loop over modules, clearing clipSize if applicable, and group modules based on attributes
        for (duration, capNeed, clipSize, disableStagger, reloadTime) in self.modules:
            if self.scale:
                duration, capNeed = self.scale_activation(duration, capNeed)

            # set clipSize to infinite if reloads are disabled unless it's
            # a cap booster module.
            if not self.reload and capNeed > 0:
                clipSize = 0
                reloadTime = 0

            # Group modules based on their properties
            if (duration, capNeed, clipSize, disableStagger, reloadTime) in mods:
                mods[(duration, capNeed, clipSize, disableStagger, reloadTime)] += 1
            else:
                mods[(duration, capNeed, clipSize, disableStagger, reloadTime)] = 1

        # Loop over grouped modules, configure staggering and push to the simulation state
        for (duration, capNeed, clipSize, disableStagger, reloadTime), amount in mods.iteritems():
            if self.stagger and not disableStagger:
                if clipSize == 0:
                    duration = int(duration / amount)
                else:
                    stagger_amount = (duration * clipSize + reloadTime) / (amount * clipSize)
                    for i in range(1, amount):
                        heapq.heappush(self.state,
                                       [i * stagger_amount, duration,
                                        capNeed, 0, clipSize, reloadTime])
            else:
                capNeed *= amount

            period = lcm(period, duration)

            # period optimization doesn't work when reloads are active.
            if clipSize:
                disable_period = True

            heapq.heappush(self.state, [0, duration, capNeed, 0, clipSize, reloadTime])

        if disable_period:
            self.period = self.t_max
        else:
            self.period = period

    def run(self):
        """Run the simulation"""

        start = time.time()

        self.reset()

        push = heapq.heappush
        pop = heapq.heappop

        state = self.state
        stability_precision = self.stability_precision
        period = self.period

        iterations = 0

        capCapacity = self.capacitorCapacity
        tau = self.capacitorRecharge / 5.0

        cap_wrap = capCapacity  # cap value at last period
        cap_lowest = capCapacity  # lowest cap value encountered
        cap_lowest_pre = capCapacity  # lowest cap value before activations
        cap = capCapacity  # current cap value
        t_wrap = self.period  # point in time of next period

        t_last = 0
        t_max = self.t_max

        while 1:
            activation = pop(state)
            t_now, duration, capNeed, shot, clipSize, reloadTime = activation
            if t_now >= t_max:
                break

            cap = ((1.0 + (sqrt(cap / capCapacity) - 1.0) * exp((t_last - t_now) / tau)) ** 2) * capCapacity

            if t_now != t_last:
                if cap < cap_lowest_pre:
                    cap_lowest_pre = cap
                if t_now == t_wrap:
                    # history is repeating itself, so if we have more cap now than last
                    # time this happened, it is a stable setup.
                    if cap >= cap_wrap:
                        break
                    cap_wrap = round(cap, stability_precision)
                    t_wrap += period

            cap -= capNeed
            if cap > capCapacity:
                cap = capCapacity

            iterations += 1

            t_last = t_now

            if cap < cap_lowest:
                if cap < 0.0:
                    break
                cap_lowest = cap

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
        push(state, activation)

        # update instance with relevant results.
        self.t = t_last
        self.iterations = iterations

        # calculate EVE's stability value
        try:
            avgDrain = reduce(float.__add__, map(lambda x: x[2] / x[1], self.state), 0.0)
            self.cap_stable_eve = 0.25 * (1.0 + sqrt(-(2.0 * avgDrain * tau - capCapacity) / capCapacity)) ** 2
        except ValueError:
            self.cap_stable_eve = 0.0

        if cap > 0.0:
            # capacitor low/high water marks
            self.cap_stable_low = cap_lowest
            self.cap_stable_high = cap_lowest_pre
        else:
            self.cap_stable_low = \
                self.cap_stable_high = 0.0

        self.runtime = time.time() - start
