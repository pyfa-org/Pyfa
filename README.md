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
