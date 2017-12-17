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

Below, for reference, is upstream's original README in its entirety. To test this fork, please refer to the [FAQ](https://github.com/pyfa-org/Pyfa/wiki/FAQ#requirements-for-running-pyfa-from-source) and [Setting Up Development Environment](https://github.com/pyfa-org/Pyfa/wiki/Setting-Up-Development-Environment) for notes on how to run from source.

# pyfa

[![Join us on Slack!](https://pyfainvite.azurewebsites.net/badge.svg)](https://pyfainvite.azurewebsites.net/) [![Build Status](https://travis-ci.org/pyfa-org/Pyfa.svg?branch=master)](https://travis-ci.org/pyfa-org/Pyfa)

![pyfa](https://cloud.githubusercontent.com/assets/3904767/10271512/af385ef2-6ade-11e5-8f67-52b8b1e4c797.PNG)

## What is it?

pyfa, short for **py**thon **f**itting **a**ssistant, allows you to create, experiment with, and save ship fittings without being in game. Open source and written in Python, it is available on any platform where Python 2.x and wxWidgets are available, including Windows, Mac OS X, and Linux.

## Latest Version and Changelogs
The latest version along with release notes can always be found on the project's [Releases](https://github.com/DarkFenX/Pyfa/releases) page. pyfa will notify you if you are running an outdated version.

## Installation
Windows and OS X users are supplied self-contained builds of pyfa on the [latest releases](https://github.com/pyfa-org/Pyfa/releases/latest) page. An `.exe` installer is also available for Windows builds. Linux users can run pyfa using their distribution's Python interpreter. There is no official self-contained package for Linux, however, there are a number of third-party packages available through distribution-specific repositories.

#### OS X
There are two different distributives for OS X: `-mac` and `-mac-deprecated`. 

* `-mac`: based on wxPython 3.0.2.0 and has updated libraries. This is the recommended build.
* `-mac-deprecated`: utilizes older binaries running on wxPython 2.8; because of this, some features are not available (currently CREST support and Attribute Overrides). Additionally, as development happens primarily on wxPython 3.0, a few GUI bugs may pop up as `-mac-deprecated` is not actively tested. However, due to some general issues with wxPython 3.0, especially on some newer OS X versions, `-mac-deprecated` is still offered for those that need it.

There is also a [Homebrew](http://brew.sh) option for installing pyfa on OS X. Please note this is maintained by a third-party and is not tested by pyfa developers. Simply fire up in terminal:
```
$ brew install Caskroom/cask/pyfa
```

### Linux Distro-specific Packages
The following is a list of pyfa packages available for certain distributions. Please note that these packages are maintained by third-parties and are not evaluated by the pyfa developers.

* Debian/Ubuntu/derivitives: https://github.com/AdamMajer/Pyfa/releases
* Arch: https://aur.archlinux.org/packages/pyfa/
* openSUSE: https://build.opensuse.org/package/show/home:rmk2/pyfa
* FreeBSD: http://www.freshports.org/games/pyfa/ (see [#484](https://github.com/pyfa-org/Pyfa/issues/484) for instructions)

### Dependencies
If you wish to help with development or simply need to run pyfa through a Python interpreter, the following software is required:

* Python 2.7
* `wxPython` 2.8/3.0
* `sqlalchemy` >= 1.0.5
* `dateutil`
* `matplotlib` (for some Linux distributions you may need to install separate wxPython bindings such as `python-matplotlib-wx`)
* `requests`
* `logbook` >= 1.0.0

## Bug Reporting
The preferred method of reporting bugs is through the project's [GitHub Issues interface](https://github.com/pyfa-org/Pyfa/issues). Alternatively, posting a report in the [pyfa thread](http://forums.eveonline.com/default.aspx?g=posts&t=247609) on the official EVE Online forums is acceptable. Guidelines for bug reporting can be found on [this wiki page](https://github.com/DarkFenX/Pyfa/wiki/Bug-Reporting). 

## License
pyfa is licensed under the GNU GPL v3.0, see LICENSE

## Resources
* Development repository: [https://github.com/pyfa-org/Pyfa](https://github.com/pyfa-org/Pyfa)
* [EVE forum thread](https://forums.eveonline.com/t/27156)
* [EVE University guide using pyfa](http://wiki.eveuniversity.org/Guide_to_using_PYFA)
* [EVE Online website](http://www.eveonline.com/)

## Contacts:
* Sable Blitzmann
    * GitHub: @blitzmann
    * [TweetFleet Slack](https://www.fuzzwork.co.uk/tweetfleet-slack-invites/): @blitzmann
    * [Gitter chat](https://gitter.im/pyfa-org/Pyfa): @ blitzmann
    * Email: sable.blitzmann@gmail.com

## CCP Copyright Notice
EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to pyfa to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, pyfa. CCP is in no way responsible for the content on or functioning of this program, nor can it be liable for any damage arising from the use of this program.
