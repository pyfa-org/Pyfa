# pyfa-taleden

## Changes In This Fork

The primary purpose of this fork is to introduce a new "DPS Simulator" in the Graph window which functions much like EFT's damage graph:

* Multiple attackers and targets may be graphed simultaneously; plots of DPS by distance are calculated for each pair and rendered on the same axes for easy comparisons.
* An attacker must be a saved fit; any fit can be dragged onto the Attackers list to add it, and currently opened fits can be added using the right-click context menu on the Attackers list.
* A target may be either a saved fit or a target profile (previously called "target resists"); target fits can be added in the same ways, but target profiles can only be added by right-click (as there is no good place to drag them from).
* Attackers and targets can both be removed by double-clicking them in their respective list.
* Left-click on a line in the plot to select it; that line then becomes thicker and a caption appears to identify the corresponding attacker and target. The line's color can also be changed by clicking on the matching colored box beside the line caption.
* Right-click on the plot to set a marker at a specific range; each plot will also show an annotation of its exact DPS value at that range.
* Set attacker and target velocity vectors using the graphical vector widgets above the attacker and target lists; left-click to set to any values, right-click to snap to 15&deg;/5% increments, or mouse wheel to change only the speed (as a percentage of maximum).
* For target fits, damage resistances can be ignored, calculated only for a specific layer (hull/armor/shield), or weighted by layer hitpoints (the default). Target profiles have only one set of resistances, so they can only be ignored or considered (any other setting).

A few small changes are also made elsewhere to support the new DPS Simulator graph:

* "Target resists" are now called "target profiles" and may optionally specify the target's signature radius and velocity in addition to its damage type resistances.
* Existing profiles will default to 0 (or blank) for both new values, which will ignore those attributes for applied damage calculations (a signature radius of 0 is treated as infinite).
* When a target profile is selected in an open fit's Firepower panel, the displayed effective firepower will reflect a "best-case scenario" in which range and transversal are zero, but the target's signature radius is still considered.
* Consequently, effective turret damage will appear slightly higher than before since signature radius does not impact turret damage with zero transversal, but the signature radius calculation still factors in wrecking shots which were previously ignored.
* Conversely, effective missile damage may appear lower than before unless the target's signature radius is larger than the missile's explosion radius. Any activated target painters or missile guidance computers on the fit will be factored in, however.

## Screenshots

![DPS Simulator](https://i.imgur.com/HVwtnba.png)

![Target Profile Editor](https://i.imgur.com/ugKq1Pm.png)

# pyfa-org (upstream)

Refer to [README.md](https://github.com/taleden/Pyfa/blob/master/README.md) for information about the original upstream project. To test this fork, please refer to the [FAQ](https://github.com/pyfa-org/Pyfa/wiki/FAQ#requirements-for-running-pyfa-from-source) and [Setting Up Development Environment](https://github.com/pyfa-org/Pyfa/wiki/Setting-Up-Development-Environment) for notes on how to run from source.
