#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import eos.db
import eos.types

class ImportError(Exception):
    pass

class defaultDatabaseValues():
    instance = None
    @classmethod

    def importDefaults(self):
        damageProfileList = []
        damageProfileList.append(["Uniform", "25", "25", "25", "25"])
        damageProfileList.append(["[Generic)EM", "100", "0", "0", "0"])
        damageProfileList.append(["[Generic)Thermal", "0", "100", "0", "0"])
        damageProfileList.append(["[Generic)Kinetic", "0", "0", "100", "0"])
        damageProfileList.append(["[Generic)Explosive", "0", "0", "0", "100"])
        damageProfileList.append(["[NPC)[Asteroid) Blood Raiders", "5067", "4214", "0", "0"])
        damageProfileList.append(["[Bombs)Concussion Bomb", "0", "0", "6400", "0"])
        damageProfileList.append(["[Bombs)Electron Bomb", "6400", "0", "0", "0"])
        damageProfileList.append(["[Bombs)Scorch Bomb", "0", "6400", "0", "0"])
        damageProfileList.append(["[Bombs)Shrapnel Bomb", "0", "0", "0", "6400"])
        damageProfileList.append(["[Frequency Crystals)[T2) Gleam", "56", "56", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)[T2) Aurora", "40", "24", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)[T2) Scorch", "72", "16", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)[T2) Conflagration", "61.6", "61.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Gamma", "61.6", "35.2", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Infrared", "44", "17.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Microwave", "35.2", "17.6", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Multifrequency", "61.6", "44", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Radio", "44", "0", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Standard", "44", "26.4", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Ultraviolet", "52.8", "26.4", "0", "0"])
        damageProfileList.append(["[Frequency Crystals)Xray", "52.8", "35.2", "0", "0"])
        damageProfileList.append(["[Hybrid Charges)[T2) Void", "0", "61.6", "61.6", "0"])
        damageProfileList.append(["[Hybrid Charges)[T2) Null", "0", "48", "40", "0"])
        damageProfileList.append(["[Hybrid Charges)[T2) Javelin", "0", "64", "48", "0"])
        damageProfileList.append(["[Hybrid Charges)[T2) Spike", "0", "32", "32", "0"])
        damageProfileList.append(["[Hybrid Charges)Antimatter", "0", "48", "67.2", "0"])
        damageProfileList.append(["[Hybrid Charges)Iridium", "0", "28.8", "38.4", "0"])
        damageProfileList.append(["[Hybrid Charges)Iron", "0", "19.2", "28.8", "0"])
        damageProfileList.append(["[Hybrid Charges)Lead", "0", "28.8", "48", "0"])
        damageProfileList.append(["[Hybrid Charges)Plutonium", "0", "48", "57.6", "0"])
        damageProfileList.append(["[Hybrid Charges)Thorium", "0", "38.4", "48", "0"])
        damageProfileList.append(["[Hybrid Charges)Tungsten", "0", "19.2", "38.4", "0"])
        damageProfileList.append(["[Hybrid Charges)Uranium", "0", "38.4", "57.6", "0"])
        damageProfileList.append(["[Missiles)Mjolnir", "100", "0", "0", "0"])
        damageProfileList.append(["[Missiles)Inferno", "0", "100", "0", "0"])
        damageProfileList.append(["[Missiles)Scourge", "0", "0", "100", "0"])
        damageProfileList.append(["[Missiles)Nova", "0", "0", "0", "100"])
        damageProfileList.append(["[Missiles)[Structure) Standup Missile", "100", "100", "100", "100"])
        damageProfileList.append(["[Projectile Ammo)[T2) Tremor", "0", "0", "24", "40"])
        damageProfileList.append(["[Projectile Ammo)[T2) Quake", "0", "0", "40", "72"])
        damageProfileList.append(["[Projectile Ammo)[T2) Hail", "0", "0", "26.4", "96.8"])
        damageProfileList.append(["[Projectile Ammo)[T2) Barrage", "0", "0", "40", "48"])
        damageProfileList.append(["[Projectile Ammo)Carbonized Lead", "0", "0", "35.2", "8.8"])
        damageProfileList.append(["[Projectile Ammo)Depleted Uranium", "0", "26.4", "17.6", "26.4"])
        damageProfileList.append(["[Projectile Ammo)EMP", "79.2", "0", "8.8", "17.6"])
        damageProfileList.append(["[Projectile Ammo)Fusion", "0", "0", "17.6", "88"])
        damageProfileList.append(["[Projectile Ammo)Nuclear", "0", "0", "8.8", "35.2"])
        damageProfileList.append(["[Projectile Ammo)Phased Plasma", "0", "88", "17.6", "0"])
        damageProfileList.append(["[Projectile Ammo)Proton", "26.4", "0", "17.6", "0"])
        damageProfileList.append(["[Projectile Ammo)Titanium Sabot", "0", "0", "52.8", "176"])
        damageProfileList.append(["[NPC (Burner)) Cruor (Blood Raiders)", "90", "90", "0", "0"])
        damageProfileList.append(["[NPC (Burner)) Dramiel (Angel)", "55", "0", "20", "96"])
        damageProfileList.append(["[NPC (Burner)) Daredevil (Serpentis)", "0", "110", "154", "0"])
        damageProfileList.append(["[NPC (Burner)) Succubus (Sanshas Nation)", "135", "30", "0", "0"])
        damageProfileList.append(["[NPC (Burner)) Worm (Guristas)", "0", "0", "228", "0"])
        damageProfileList.append(["[NPC (Burner)) Enyo", "0", "147", "147", "0"])
        damageProfileList.append(["[NPC (Burner)) Hawk", "0", "0", "247", "0"])
        damageProfileList.append(["[NPC (Burner)) Jaguar", "36", "0", "50", "182"])
        damageProfileList.append(["[NPC (Burner)) Vengeance", "232", "0", "0", "0"])
        damageProfileList.append(["[NPC (Burner)) Ashimmu (Blood Raiders)", "260", "100", "0", "0"])
        damageProfileList.append(["[NPC (Burner)) Talos", "0", "413", "413", "0"])
        damageProfileList.append(["[NPC (Burner)) Sentinel", "0", "75", "0", "90"])
        damageProfileList.append(["[NPC)[Asteroid) Angel Cartel", "1838", "562", "2215", "3838"])
        damageProfileList.append(["[NPC)[Deadspace) Angel Cartel", "369", "533", "1395", "3302"])
        damageProfileList.append(["[NPC)[Deadspace) Blood Raiders", "6040", "5052", "10", "15"])
        damageProfileList.append(["[NPC)[Asteroid) Guristas", "0", "1828", "7413", "0"])
        damageProfileList.append(["[NPC)[Deadspace) Guristas", "0", "1531", "9680", "0"])
        damageProfileList.append(["[NPC)[Asteroid) Rogue Drone", "394", "666", "1090", "1687"])
        damageProfileList.append(["[NPC)[Deadspace) Rogue Drone", "276", "1071", "1069", "871"])
        damageProfileList.append(["[NPC)[Asteroid) Sanshas Nation", "5586", "4112", "0", "0"])
        damageProfileList.append(["[NPC)[Deadspace) Sanshas Nation", "3009", "2237", "0", "0"])
        damageProfileList.append(["[NPC)[Asteroid) Serpentis", "0", "5373", "4813", "0"])
        damageProfileList.append(["[NPC)[Deadspace) Serpentis", "0", "3110", "1929", "0"])
        damageProfileList.append(["[NPC)[Mission) Amarr Empire", "4464", "3546", "97", "0"])
        damageProfileList.append(["[NPC)[Mission) Caldari State", "0", "2139", "4867", "0"])
        damageProfileList.append(["[NPC)[Mission) CONCORD", "336", "134", "212", "412"])
        damageProfileList.append(["[NPC)[Mission) Gallente Federation", "9", "3712", "2758", "0"])
        damageProfileList.append(["[NPC)[Mission) Khanid", "612", "483", "43", "6"])
        damageProfileList.append(["[NPC)[Mission) Minmatar Republic", "1024", "388", "1655", "4285"])
        damageProfileList.append(["[NPC)[Mission) Mordus Legion", "25", "262", "625", "0"])
        damageProfileList.append(["[NPC)[Mission) Thukker", "0", "52", "10", "79"])
        damageProfileList.append(["[NPC)[Other) Sleepers", "1472", "1472", "1384", "1384"])
        damageProfileList.append(["[NPC)[Other) Sansha Incursion", "1682", "1347", "3678", "3678"])
        for damageProfileRow in damageProfileList:
            damageProfile = eos.db.getDamagePattern(damageProfileRow[0])
            if damageProfile is None:
                damageProfile = eos.types.DamagePattern(damageProfileRow[1], damageProfileRow[2], damageProfileRow[3], damageProfileRow[4])
                damageProfile.name = damageProfileRow[0]
                eos.db.save(damageProfile)

        targetResistProfileList = []
        targetResistProfileList.append(["Uniform", "25.0", "25.0", "25.0", "25.0"])
        targetResistProfileList.append(["[NPC][Other] Sleepers", "276344.0", "282094.0", "276344.0", "276344.0"])
        targetResistProfileList.append(["[NPC][Other] Sansha Incursion", "3426857.48", "3426682.48", "3427332.48", "3428257.48"])
        targetResistProfileList.append(["[NPC][Mission] Thukker", "2634.0", "2515.5", "3055.5", "3277.0"])
        targetResistProfileList.append(["[NPC][Mission] Mordus Legion", "36159.5", "34354.25", "25749.25", "30217.5"])
        targetResistProfileList.append(["[NPC][Mission] Minmatar Republic", "589004.85", "503918.35", "433839.85", "353693.35"])
        targetResistProfileList.append(["[NPC][Mission] Khanid", "15507.25", "19317.25", "24721.25", "29248.25"])
        targetResistProfileList.append(["[NPC][Mission] Gallente Federation", "424438.0", "359996.2", "304695.75", "491406.5"])
        targetResistProfileList.append(["[NPC][Mission] Caldari State", "566594.5", "420853.5", "347228.0", "496174.25"])
        targetResistProfileList.append(["[NPC][Mission] CONCORD", "31078.75", "30868.75", "31078.75", "31078.75"])
        targetResistProfileList.append(["[NPC][Mission] Amarr Empire", "342504.0", "412979.95", "485898.25", "556514.0"])
        targetResistProfileList.append(["[NPC][Deadspace] Serpentis", "193953.25", "163280.0", "132962.25", "225117.25"])
        targetResistProfileList.append(["[NPC][Deadspace] Sanshas Nation", "145001.25", "180259.5", "215316.0", "250180.75"])
        targetResistProfileList.append(["[NPC][Deadspace] Rogue Drone", "101197.1", "119606.05", "140270.65", "159592.2"])
        targetResistProfileList.append(["[NPC][Deadspace] Guristas", "258913.25", "188927.75", "153524.75", "224637.5"])
        targetResistProfileList.append(["[NPC][Deadspace] Blood Raiders", "152864.5", "188922.8", "224795.0", "260472.0"])
        targetResistProfileList.append(["[NPC][Deadspace] Angel Cartel", "266066.85", "229245.35", "193690.6", "157547.1"])
        targetResistProfileList.append(["[NPC][Asteroid] Serpentis", "306253.74", "274712.59", "253115.29", "339831.19"])
        targetResistProfileList.append(["[NPC][Asteroid] Sanshas Nation", "259921.52", "283226.65", "322865.57", "357884.28"])
        targetResistProfileList.append(["[NPC][Asteroid] Rogue Drone", "138988.6", "169915.05", "203907.15", "236665.7"])
        targetResistProfileList.append(["[NPC][Asteroid] Guristas", "333718.82", "266658.76", "228592.64", "296350.35"])
        targetResistProfileList.append(["[NPC][Asteroid] Blood Raiders", "253672.83", "282098.6", "326577.52", "362882.07"])
        targetResistProfileList.append(["[NPC][Asteroid] Angel Cartel", "283011.68", "252440.67", "230021.79", "200059.26"])
        targetResistProfileList.append(["[NPC (Burner)] Worm (Guristas)", "2787.0", "3193.0", "3501.0", "3583.0"])
        targetResistProfileList.append(["[NPC (Burner)] Vengeance", "2153.1", "1997.6", "2979.75", "3454.1"])
        targetResistProfileList.append(["[NPC (Burner)] Talos", "4470.0", "4440.0", "4980.0", "4260.0"])
        targetResistProfileList.append(["[NPC (Burner)] Succubus (Sanshas Nation)", "1805.0", "2130.0", "2495.0", "2700.0"])
        targetResistProfileList.append(["[NPC (Burner)] Sentinel", "3545.0", "2850.0", "3425.0", "4350.0"])
        targetResistProfileList.append(["[NPC (Burner)] Jaguar", "2760.02", "2273.37", "1580.76", "1741.44"])
        targetResistProfileList.append(["[NPC (Burner)] Hawk", "1142.9", "2998.82", "2677.29", "2000.35"])
        targetResistProfileList.append(["[NPC (Burner)] Enyo", "1910.07", "2598.33", "3147.09", "1025.76"])
        targetResistProfileList.append(["[NPC (Burner)] Dramiel (Angel)", "1729.0", "1734.0", "1907.0", "1900.0"])
        targetResistProfileList.append(["[NPC (Burner)] Daredevil (Serpentis)", "1855.0", "1775.0", "1955.0", "1635.0"])
        targetResistProfileList.append(["[NPC (Burner)] Cruor (Blood Raiders)", "7460.0", "7170.0", "7170.0", "7150.0"])
        targetResistProfileList.append(["[NPC (Burner)] Ashimmu (Blood Raiders)", "8480.0", "8800.0", "8720.0", "9240.0"])


        for targetResistProfileRow in targetResistProfileList:
            resistsProfile = eos.db.getTargetResists(targetResistProfileRow[0])
            if resistsProfile is None:
                resistsProfile = eos.types.eos.types.TargetResists(targetResistProfileRow[1], targetResistProfileRow[2], targetResistProfileRow[3], targetResistProfileRow[4])
                resistsProfile.name = targetResistProfileRow[0]
                eos.db.save(resistsProfile)
