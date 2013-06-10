#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from eos.types import Slot, Fit, Module, State
import random
import copy
import math
import bisect
import itertools
import time

class SlotFill(object):
    def __init__(self, original, modules, attributeWeights=None, propertyWeights=None, specificWeights=None, defaultState = State.ACTIVE):
        self.original = original
        self.attributeWeights = attributeWeights or {}
        self.propertyWeights = propertyWeights or {}
        self.specificWeights = specificWeights or []
        self.state = State.ACTIVE
        self.modules = map(self.__newModule, modules)

    def __newModule(self, item):
        m = Module(item)
        m.state = self.state
        return m

    def __getMetaParent(self, item):
        metaGroup = item.metaGroup
        return item if metaGroup is None else metaGroup.parent

    def fitness(self, fit, chromosome):
        modList = fit.modules
        modAttr = fit.ship.getModifiedItemAttr

        modList.extend(chromosome)
        fit.clear()
        fit.calculateModifiedAttributes()

        if not fit.fits:
            del modList[-len(chromosome):]
            return 0

        weight = 0
        for attr, value in self.attributeWeights.iteritems():
            weight += modAttr(attr) * (value if value >= 0 else 1.0 / -value)

        for prop, value in self.propertyWeights.iteritems():
            weight += getattr(fit, prop) * (value if value >= 0 else 1.0 / -value)

        for specific in self.specificWeights:
            weight += specific(fit)

        totalVars = (fit.ship.getModifiedItemAttr("powerOutput"),
                     fit.ship.getModifiedItemAttr("cpuOutput"),
                     fit.ship.getModifiedItemAttr('upgradeCapacity'))

        usedVars = (fit.pgUsed, fit.cpuUsed, fit.calibrationUsed)

        total = 0
        used = 0
        for tv, uv in zip(totalVars, usedVars):
            if uv > tv:
                del modList[-len(chromosome):]
                return 0

        del modList[-len(chromosome):]


        return weight


    def run(self, elite = 0.05, crossoverChance = 0.8, slotMutationChance = 0.5, typeMutationChance = 0.5):
        #Use a copy of the original for all our calcs. We don't want to damage it
        fit = copy.deepcopy(self.original)
        fit.unfill()

        #First of all, lets check the number of slots we got to play with
        chromLength = -1
        slotAmounts = {}
        for type in Slot.getTypes():
            slot = Slot.getValue(type)
            amount = fit.getSlotsFree(slot)
            if amount > 0:
                slotAmounts[slot] = amount

            chromLength += amount

        if not slotAmounts:
            #Nothing to do, joy
            return

        slotModules = {}
        metaModules = {}

        for slotType in slotAmounts:
            slotModules[slotType] = modules = []

        for module in self.modules:
            #Store the variations of each base for ease and speed
            metaParent = self.__getMetaParent(module.item)
            metaList = metaModules.get(metaParent)
            if metaList is None:
                metaList = metaModules[metaParent] = []
            metaList.append(module)

            #Sort stuff by slotType for ease and speed
            slot = module.slot
            if slot in slotModules:
                slotModules[slot].append(module)

        for slotType, modules in slotModules.iteritems():
            if len(modules) == 0:
                chromLength -= slotAmounts[slotType]
                del slotAmounts[slotType]

        #Now, we need an initial set, first thing to do is decide how big that set will be
        setSize = 10

        #Grab some variables locally for performance improvements
        rchoice = random.choice
        rrandom = random.random
        rrandint = random.randint
        bbisect = bisect.bisect
        ccopy = copy.copy

        #Get our list for storage of our chromosomes
        chromosomes = []

        # Helpers
        weigher = lambda chromosome: (self.fitness(fit, chromosome), chromosome)
        keyer = lambda info: info[0]

        eliteCutout = int(math.floor(setSize * (1 - elite)))
        lastEl = setSize - 1

        #Generate our initial set entirely randomly
        #Subtelies to take in mind:
        # * modules of the same slotType are kept together for easy cross-overing
        state = self.state
        for _ in xrange(setSize):
            chrom = []
            for type, amount in slotAmounts.iteritems():
                for _ in xrange(amount):
                    chrom.append(rchoice(slotModules[type]))

            chromosomes.append(weigher(chrom))

        #Sort our initial set
        chromosomes.sort(key=keyer)
        currentGeneration = chromosomes

        #Yield the best result from our initial set, this is gonna be pretty bad
        yield currentGeneration[lastEl]

        #Setup's done, now we can actualy apply our genetic algorithm to optimize all this
        while True:
            moo = time.time()
            #First thing we do, we're gonna be elitair
            #Grab the top x%, we'll put em in the next generation
            nextGeneration = []
            for i in xrange(lastEl, eliteCutout - 1, -1):
                nextGeneration.append(currentGeneration[i])

            #Figure out our ratios to do our roulette wheel
            fitnessList = map(keyer, currentGeneration)
            totalFitness = float(sum(fitnessList))

            curr = 0
            ratios = []
            for fitness in fitnessList:
                curr += fitness
                ratios.append(curr / (totalFitness or 1))

            t = 0
            #Do our pairing
            for _ in xrange(0, eliteCutout):
                # Crossover chance
                mother = currentGeneration[bbisect(ratios, rrandom())][1]
                father = currentGeneration[bbisect(ratios, rrandom())][1]
                if rrandom() <= crossoverChance:
                    crosspoint = rrandint(0, chromLength)
                    luke = mother[:crosspoint] + father[crosspoint:]
                else:
                    luke = father

                #Chance for slot mutation
                if rrandom() <= slotMutationChance:
                    target = rrandint(0, chromLength)
                    mod = luke[target]
                    luke[target] = rchoice(slotModules[mod.slot])

                if rrandom() <= typeMutationChance:
                    #Mutation of an item to another one of the same type
                    target = rrandint(0, chromLength)
                    mod = luke[target]
                    vars = metaModules[self.__getMetaParent(mod.item)]
                    luke[target] = rchoice(vars)

                tt = time.time()
                nextGeneration.append(weigher(luke))
                t += time.time() - tt

            print "time spent weighing: ", t

            nextGeneration.sort(key=keyer)
            currentGeneration = nextGeneration
            print "total time spent this iteration:", time.time() - moo
            yield currentGeneration[lastEl]
